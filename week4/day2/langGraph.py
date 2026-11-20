from typing import TypedDict
from langgraph.graph import StateGraph, END #type: ignore



# State
class State(TypedDict):
    number: int

# Node 1: double the number
def double(state: State) -> dict:
    newnum = state["number"] * 2
    print("in double")
    print(newnum)
    return {"number": newnum}

# Node 2: finish
def finish(state: State) -> dict:
    print("in finish")
    print(state["number"])
    return {"number": state["number"]}

# Decision: which node runs next?
def decision(state: State) -> str:
    if state["number"] < 100:
        return "double"
    else:
        return "finish"


# Build the graph
builder = StateGraph(State)
builder.add_node("double", double)
builder.add_node("finish", finish)


# Entry point
builder.set_entry_point("double")

# Conditional edge
builder.add_conditional_edges(
    "double",
    decision,
    {"double": "double", "finish": "finish"},
)

builder.add_edge("finish", END)
graph = builder.compile()


# result = graph.invoke({"number": 5})
# print("Final result:", result)

# This means run the code below only if this file is the one being run directly.
if __name__ == "__main__":
    result = graph.invoke({"number": 5})
    print("Final result:", result)  