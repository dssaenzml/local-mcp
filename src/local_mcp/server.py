import sys
import logging

import click
from pydantic import Field

from fastmcp import FastMCP, Context

from starlette.requests import Request
from starlette.responses import PlainTextResponse

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# In-memory state
# ----------------------------------------------------------------------------
notes: dict[str, str] = {}

# ----------------------------------------------------------------------------
# Create the FastMCP server instance globally
# ----------------------------------------------------------------------------
mcp = FastMCP("local-mcp")

# ----------------------------------------------------------------------------
# Resources
# ----------------------------------------------------------------------------
@mcp.resource("note://{name}")
async def get_note(
    name: str = Field(..., description="Name of the note to get"),
    ctx: Context = None,
) -> str:
    """Return the content of a note by name."""
    await ctx.info(f"Getting note '{name}'")
    if name not in notes:
        raise ValueError(f"Note '{name}' not found")
    return notes[name]


# ----------------------------------------------------------------------------
# Prompts
# ----------------------------------------------------------------------------
@mcp.prompt(name="summarize-notes")
async def summarize_notes(
    style: str | None = None,
    ctx: Context = None,
) -> str:
    """Return a prompt asking the LLM to summarize all notes in the desired style."""
    await ctx.info(f"Summarizing notes with style: {style}")
    detail = " Give extensive details." if style == "detailed" else ""
    content = "Here are the current notes to summarize:" + detail + "\n\n" + "\n".join(
        f"- {n}: {c}" for n, c in notes.items()
    )
    return content


# ----------------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------------
@mcp.tool(name="add-note", description="Add a new note to the server")
async def add_note(
    name: str = Field(..., description="Name of the note"),
    content: str = Field(..., description="Content of the note"),
    ctx: Context = None,
) -> dict:
    """Create or overwrite a note, returning confirmation text."""
    await ctx.info(f"Added note '{name}' with content: {content}")
    notes[name] = content
    result = {
        "result": f"Added note '{name}' with content: {content}",
    }
    return result


@mcp.tool(name="list-notes", description="List all notes on the server")
async def list_notes(ctx: Context = None) -> list[str]:
    """List all notes on the server""" 
    await ctx.info(f"Listing notes: {list(notes.keys())}")
    return list(notes.keys())


@mcp.tool(name="delete-note", description="Delete a note from the server")
async def delete_note(
    name: str = Field(..., description="Name of the note to delete"),
    ctx: Context = None,
) -> str:
    """Delete a note from the server"""
    if name not in notes:
        await ctx.error(f"Note '{name}' not found on server")
        raise ValueError(f"Note '{name}' not found on server")
    
    del notes[name]
    await ctx.info(f"Deleted note '{name}' from server")
    return f"Deleted note '{name}' from server"


@mcp.tool(name="get-note-content", description="Get a note content from the server")
async def get_note_content(
    name: str = Field(..., description="Name of the note to get content from"),
    ctx: Context = None,
) -> str:
    """Get a note content from the server"""
    if name not in notes:
        await ctx.error(f"Note '{name}' not found on server")
        raise ValueError(f"Note '{name}' not found on server")
    
    await ctx.info(f"Retrieved content for note '{name}'")
    return notes[name]


@mcp.tool(name="add", description="Add two numbers")
async def add(
    a: int = Field(..., description="First number"),
    b: int = Field(..., description="Second number"),
    ctx: Context = None,
    ) -> int:
    """Add two numbers"""
    result = a + b
    await ctx.info(f"Adding {a} + {b} = {result}")
    return result


@mcp.tool(name="calculate-bmi", description="Calculate BMI")
async def calculate_bmi(
    weight_kg: float = Field(..., description="Weight in kilograms"),
    height_m: float = Field(..., description="Height in meters"),
    ctx: Context = None,
    ) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    result = weight_kg / (height_m**2)
    await ctx.info(f"Calculated BMI: {result}")
    return result


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


# ----------------------------------------------------------------------------
# CLI command
# ----------------------------------------------------------------------------
@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport type",
)
@click.option("--port", default=8000, help="Port to listen on for Streamable HTTP")
@click.option("--host", default="localhost", help="Host to bind to for Streamable HTTP")
@click.option("--path", default="/mcp", help="Path to bind to for Streamable HTTP")
@click.option(
    "--log-level", 
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level",
    )
def main(port: int, transport: str, host: str, path: str, log_level: str) -> None:
    """Run the MCP server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting MCP server with transport: {transport}")
    
    try:
        if transport == "http":
            logger.info(f"Streamable HTTP server will be available at http://{host}:{port}{path}")
            mcp.run(
                transport=transport,
                host=host,
                port=port,
                path=path,
                log_level=log_level,
            )
        else:
            mcp.run(
                transport=transport,
            )
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)


# ----------------------------------------------------------------------------
# Entrypoint (for direct execution)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
