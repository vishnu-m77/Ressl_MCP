#!/usr/bin/env python3

import asyncio
import json
from pathlib import Path
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


app = Server("file-search-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_in_file",
            description="Searches for a keyword within a file and returns matching lines with line numbers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filePath": {"type": "string", "description": "Path to the file to search"},
                    "keyword": {"type": "string", "description": "Keyword to search for"},
                    "caseSensitive": {"type": "boolean", "description": "Case-sensitive search (default: false)", "default": False},
                },
                "required": ["filePath", "keyword"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    if name != "search_in_file":
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    file_path = arguments.get("filePath")
    keyword = arguments.get("keyword")
    case_sensitive = arguments.get("caseSensitive", False)

    if not file_path or not keyword:
        return [TextContent(type="text", text=json.dumps({"error": "Both filePath and keyword are required"}))]

    resolved_path = Path(file_path).resolve()
    
    if not resolved_path.exists():
        return [TextContent(type="text", text=json.dumps({"error": f"File not found: {resolved_path}"}))]

    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": f"Error reading file: {str(e)}"}))]

    search_term = keyword if case_sensitive else keyword.lower()
    matches = []

    for index, line in enumerate(lines, start=1):
        line_to_search = line if case_sensitive else line.lower()
        if search_term in line_to_search:
            matches.append({"lineNumber": index, "content": line.rstrip("\n\r")})

    result = {
        "filePath": str(resolved_path),
        "keyword": keyword,
        "caseSensitive": case_sensitive,
        "totalMatches": len(matches),
        "matches": matches,
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
