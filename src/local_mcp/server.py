from __future__ import annotations

from pydantic import Field

from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP server instance (required for `mcp dev`)
mcp = FastMCP("local-mcp")

# ----------------------------------------------------------------------------
# In-memory state
# ----------------------------------------------------------------------------
notes: dict[str, str] = {}


# ----------------------------------------------------------------------------
# Resources
# ----------------------------------------------------------------------------
@mcp.resource("note://{name}")
def get_note(name: str) -> str:
    """Return the content of a note by name."""
    if name not in notes:
        raise ValueError(f"Note '{name}' not found")
    return notes[name]


# ----------------------------------------------------------------------------
# Prompts
# ----------------------------------------------------------------------------
@mcp.prompt(name="summarize-notes")
async def summarize_notes(style: str | None = None) -> str:
    """Return a prompt asking the LLM to summarize all notes in the desired style."""
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
    ctx: Context | None = Field(None, description="Context of the note"),
    ) -> str:
    """Create or overwrite a note, returning confirmation text."""
    notes[name] = content

    # Notify clients that new resources are available
    if ctx is not None:
        await ctx.send_resource_list_changed()

    return f"Added note '{name}' with content: {content}"


# Add an addition tool
@mcp.tool(name="add", description="Add two numbers")
def add(
    a: int = Field(..., description="First number"),
    b: int = Field(..., description="Second number"),
    ) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool(name="calculate-bmi", description="Calculate BMI")
def calculate_bmi(
    weight_kg: float = Field(..., description="Weight in kilograms"),
    height_m: float = Field(..., description="Height in meters"),
    ) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


# ----------------------------------------------------------------------------
# Entrypoint (for direct execution)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
