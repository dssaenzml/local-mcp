#!/usr/bin/env python3
"""
Test script for the local MCP server.
This demonstrates how to properly connect to and test an MCP HTTP server.
"""
import asyncio
from fastmcp import Client

async def test_mcp_server():
    """Test the MCP server running on HTTP transport."""
    
    # Connect to the MCP server (not raw HTTP requests!)
    async with Client("http://localhost:8000/mcp") as client:
        print("🔌 Connected to MCP server!")
        
        # Test basic connectivity
        await client.ping()
        print("✅ Ping successful!")
        
        # List available tools
        tools = await client.list_tools()
        print(f"\n🔧 Available tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # List available resources
        resources = await client.list_resources()
        print(f"\n📁 Available resources ({len(resources)}):")
        for resource in resources:
            print(f"  - {resource.uri}: {resource.description}")
        
        # List available prompts
        prompts = await client.list_prompts()
        print(f"\n💬 Available prompts ({len(prompts)}):")
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description}")
        
        # Test some tools
        print("\n🧪 Testing tools:")
        
        # Test add function
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"  add(5, 3) = {result.data}")
        
        # Test BMI calculator
        result = await client.call_tool("calculate-bmi", {"weight_kg": 70, "height_m": 1.75})
        print(f"  BMI(70kg, 1.75m) = {result.data:.2f}")
        
        # Test note operations
        print("\n📝 Testing note operations:")
        
        # Add a note
        await client.call_tool("add-note", {"name": "test", "content": "This is a test note"})
        print("  ✅ Added test note")
        
        # List notes
        notes = await client.call_tool("list-notes")
        print(f"  📋 Notes: {notes.data}")
        
        # Get note content
        content = await client.call_tool("get-note-content", {"name": "test"})
        print(f"  📄 Note content: {content.data}")
        
        # Test resource
        note_resource = await client.read_resource("note://test")
        print(f"  🔗 Resource content: {note_resource}")
        
        print("\n🎉 All tests passed!")

if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Make sure your MCP server is running with:")
        print("   docker run --rm -p 8000:8000 local-mcp --transport http --host 0.0.0.0 --port 8000") 