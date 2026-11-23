"""Minimal MCP server exposing a tool, a resource and a prompt.

Run:  pip install "mcp[cli]>=2"   # mcp 2.x (FastMCP was renamed to MCPServer)
      python server.py          # stdio transport (used by client.py / Claude Desktop)
"""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("demo-server")

# Fake data source
ORDERS = {
    "4521": {"item": "Pizza", "status": "delivered", "amount": 450},
    "4522": {"item": "Burger", "status": "preparing", "amount": 250},
}


# TOOL: model-controlled action
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def get_order_status(order_id: str) -> str:
    """Get the status of a restaurant order by its ID."""
    order = ORDERS.get(order_id)
    if not order:
        return f"Order {order_id} not found"
    return f"Order {order_id}: {order['item']} is {order['status']} (Rs {order['amount']})"


# RESOURCE: app-controlled context (read-only data)
@mcp.resource("orders://{order_id}")
def order_resource(order_id: str) -> str:
    """Raw order record."""
    return str(ORDERS.get(order_id, {}))


# PROMPT: user-selected reusable template
@mcp.prompt()
def summarize_order(order_id: str) -> str:
    """Prompt template to summarize an order for a customer."""
    return f"Look up order {order_id} and write a friendly 2-line status update for the customer."


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport