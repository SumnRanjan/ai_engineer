"""
Tools for the Mini Coding Agent (used by main.py).

Exports:
    TOOLS         -> tool schemas sent to the LLM (Groq / OpenAI format)
    code_files()  -> list of C++ files in the workspace
    make_tools()  -> {tool_name: python_function} bound to one workspace

All tools return plain strings, because that is what goes back to the LLM.
"""

from pathlib import Path

CODE_EXTENSIONS = {".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"}
SKIP_DIRS = {".git", ".venv", "build", "__pycache__", "node_modules"}


# ============================================================
# FILE LISTING
# ============================================================


def code_files(workspace: Path) -> list[Path]:
    """All C++ source/header files inside the workspace, sorted."""
    workspace = Path(workspace)
    if not workspace.is_dir():
        return []
    return sorted(
        p for p in workspace.rglob("*")
        if p.is_file()
        and p.suffix.lower() in CODE_EXTENSIONS
        and not any(part in SKIP_DIRS for part in p.relative_to(workspace).parts)
    )


# ============================================================
# TOOL SCHEMAS  (what the LLM sees)
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": (
                "Find which code files are related to the bug. Returns files whose name or "
                "content contains the keyword (case-insensitive), with the number of matches. "
                "An empty keyword lists all code files."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Word to search for, e.g. a function or variable name."},
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": (
                "Show lines in one file that contain the keyword, with line numbers. "
                "An empty keyword shows the whole file with line numbers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path relative to the project, as returned by search_files."},
                    "keyword": {"type": "string", "description": "Word to search for. Use \"\" to see the whole file."},
                },
                "required": ["path", "keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "replace_line",
            "description": (
                "Replace ONE whole line in a file with a new line. Take the line number from "
                "search_in_file. new_line must be a single complete line of C++ (no newlines)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path relative to the project."},
                    "line_number": {"type": "integer", "description": "1-based line number to replace."},
                    "new_line": {"type": "string", "description": "The full replacement line."},
                },
                "required": ["path", "line_number", "new_line"],
            },
        },
    },
]


# ============================================================
# TOOL FUNCTIONS  (bound to one workspace)
# ============================================================

# factory function 
def make_tools(workspace: Path) -> dict:
    """Create the tool functions for one workspace. The LLM can never touch files outside it."""
    workspace = Path(workspace).resolve()

    def _resolve(path: str) -> Path:
        """Turn the LLM's path into a real file inside the workspace, or raise a helpful error."""
        p = (workspace / path).resolve()
        if not p.is_relative_to(workspace):
            raise ValueError(f"'{path}' is outside the project. Use paths from search_files.")
        if not p.is_file():
            # forgive a bare file name like "main.cpp" when the file lives in a subfolder
            matches = [f for f in code_files(workspace) if f.name == Path(path).name]
            if len(matches) == 1:
                return matches[0]
            raise FileNotFoundError(f"'{path}' not found. Use search_files to see the available files.")
        return p

    def _rel(p: Path) -> str:
        return p.relative_to(workspace).as_posix()

    def _read_lines(p: Path) -> list[str]:
        return p.read_text(encoding="utf-8", errors="replace").splitlines()

    # ---------------- search_files ----------------
    def search_files(keyword: str = "") -> str:
        files = code_files(workspace)
        if not files:
            return "No code files in the project."

        key = keyword.strip().lower()
        if not key:
            return "All code files:\n" + "\n".join(_rel(f) for f in files)

        results = []
        for f in files:
            hits = sum(line.lower().count(key) for line in _read_lines(f))
            if key in f.name.lower() or hits:
                results.append(f"{_rel(f)}  ({hits} matches)")

        if not results:
            return (f"No file contains '{keyword}'. Try another keyword, or an empty keyword "
                    "to list all files:\n" + "\n".join(_rel(f) for f in files))
        return f"Files related to '{keyword}':\n" + "\n".join(results)

    # ---------------- search_in_file ----------------
    def search_in_file(path: str, keyword: str = "") -> str:
        p = _resolve(path)
        lines = _read_lines(p)
        key = keyword.strip().lower()

        shown = [f"{i:4}: {line}" for i, line in enumerate(lines, start=1)
                 if not key or key in line.lower()]

        if not shown:
            return f"No line in {_rel(p)} contains '{keyword}'. Use keyword \"\" to see the whole file."
        title = f"{_rel(p)} (whole file, {len(lines)} lines)" if not key else f"Lines in {_rel(p)} with '{keyword}'"
        return title + ":\n" + "\n".join(shown)

    # ---------------- replace_line ----------------
    def replace_line(path: str, line_number: int, new_line: str) -> str:
        p = _resolve(path)
        lines = _read_lines(p)
        line_number = int(line_number)

        if not 1 <= line_number <= len(lines):
            return f"Line {line_number} does not exist. {_rel(p)} has {len(lines)} lines."
        if "\n" in new_line.strip("\n"):
            return "new_line must be ONE line. Call replace_line once per line you want to change."

        old = lines[line_number - 1]
        new = new_line.rstrip("\n")

        # keep the original indentation if the LLM dropped it
        if new and not new[0].isspace():
            indent = old[: len(old) - len(old.lstrip())]
            new = indent + new

        lines[line_number - 1] = new
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")

        return (f"Replaced line {line_number} in {_rel(p)}\n"
                f"  before: {old.strip()}\n"
                f"  after : {new.strip()}")

    return {
        "search_files": search_files,
        "search_in_file": search_in_file,
        "replace_line": replace_line,
    }