from .server import mcp

def main() -> None:
    """Package entry point executed by the `local-mcp` CLI script."""
    mcp.run(transport="stdio")

# Optionally expose other important items at package level
__all__ = ['main', 'mcp']