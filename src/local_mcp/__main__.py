#!/usr/bin/env python3
"""
Entry point for the local MCP server.
"""
import sys

from local_mcp.server import main

if __name__ == "__main__":
    sys.exit(main())
