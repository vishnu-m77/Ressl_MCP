# Ressl_MCP

MCP (Model Context Protocol) server implementation with a file search tool.

## Features

- search_in_file: Searches for a specified keyword within a file and returns matching lines with line numbers
  - Supports case-sensitive and case-insensitive searches
  - Returns line numbers for easy reference
  - Handles file path resolution (relative and absolute paths)

## MCP Configuration

To use this server with an MCP client, add the following configuration:

### MCP Inspector

When using MCP Inspector, configure the server with:
- Command: `python`
- Args: `["/absolute/path/to/Ressl_MCP/src/server.py"]`

## Tool: search_in_file

### Parameters

- `filePath` (required): The path to the file to search in (relative or absolute)
- `keyword` (required): The keyword or phrase to search for
- `caseSensitive` (optional): Whether the search should be case-sensitive (default: false)

### Example Usage

Input:
```json
{
  "filePath": "sample/test.txt",
  "keyword": "sample",
  "caseSensitive": false
}
```

Output:
```json
{
  "filePath": "/absolute/path/to/Ressl_MCP/sample/test.txt",
  "keyword": "sample",
  "caseSensitive": false,
  "totalMatches": 3,
  "matches": [
    {
      "lineNumber": 1,
      "content": "This is a sample file for testing the file search tool."
    },
    {
      "lineNumber": 4,
      "content": "This line contains the word sample again."
    },
    {
      "lineNumber": 7,
      "content": "The search tool should find all occurrences."
    }
  ]
}
```

## Setup

Sample files are provided in the `sample/` directory:
- `sample/test.txt` - Simple text file with multiple occurrences of "sample"
### Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Test with MCP Inspector

1. Install Node.js and npm (if not already installed)

2. Install MCP Inspector:
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

3. Create a test configuration file (e.g., `test-config.json`):
   ```json
   {
     "mcpServers": {
       "file-search-server": {
         "command": "python",
         "args": ["/absolute/path/to/Ressl_MCP/src/server.py"]
       }
     }
   }
   ```
   Replace `/absolute/path/to/Ressl_MCP` with your actual project path.

4. Run MCP Inspector:
   ```bash
   mcp-inspector --config test-config.json
   ```

5. In MCP Inspector:
   - Select the `search_in_file` tool
   - Use the following test input:
     ```json
     {
       "filePath": "sample/test.txt",
       "keyword": "sample",
       "caseSensitive": false
     }
     ```
   - Click "Call Tool" and verify the output shows matching lines with line numbers

