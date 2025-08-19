# Sample Data MCP

A Model Context Protocol (MCP) server that generates fixed-length test data based on field specifications. This tool helps developers create realistic test datasets with customizable field types and formats.

## Features

- Generate fixed-length test data records
- Support for multiple field types:
  - `string`: Random names using Faker library
  - `enum`: Random selection from provided values
  - `integer`: Random integers within specified range
  - `date`: Random dates with customizable format
  - `filler`: Space padding fields
- Configurable field length and constraints
- MCP-compatible for integration with Claude Code

## Installation

### Prerequisites

- Python 3.13 or higher
- [UV package manager](https://docs.astral.sh/uv/)

### Install with UV

1. Clone or download this project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   uv sync
   ```

### Install into Claude Code

1. Add the MCP server to your Claude Code configuration. Edit your MCP settings file (typically `~/.config/claude-code/mcp_servers.json` or similar):

   ```json
   {
     "mcpServers": {
       "sample-data-mcp": {
         "command": "uv",
         "args": ["run", "/path/to/sample-data-mcp/main.py"],
         "cwd": "/path/to/sample-data-mcp"
       }
     }
   }
   ```

2. Restart Claude Code to load the new MCP server

## Usage

Once installed, you can use the `generate_test_data_tool` through Claude Code to create test data:

### Example Field Specification

```python
fields = [
    {
        "name": "customer_id",
        "type": "integer",
        "length": 8,
        "min": 1000,
        "max": 9999
    },
    {
        "name": "customer_name",
        "type": "string",
        "length": 25
    },
    {
        "name": "status",
        "type": "enum",
        "length": 6,
        "values": ["ACTIVE", "INACTIVE", "PENDING"]
    },
    {
        "name": "signup_date",
        "type": "date",
        "length": 8,
        "format": "%Y%m%d"
    },
    {
        "name": "filler",
        "type": "filler",
        "length": 5
    }
]
```

### Field Types

| Type | Description | Required Fields | Optional Fields |
|------|-------------|-----------------|-----------------|
| `string` | Random names | `name`, `type`, `length` | - |
| `enum` | Random selection from list | `name`, `type`, `length`, `values` | - |
| `integer` | Random integer | `name`, `type`, `length` | `min`, `max` |
| `date` | Random date | `name`, `type`, `length` | `format` |
| `filler` | Space padding | `name`, `type`, `length` | - |

## Development

### Running Locally

```bash
uv run main.py
```

### Dependencies

- `faker`: For generating realistic fake data
- `mcp`: Model Context Protocol implementation
- `pydantic`: Data validation and settings management

## License

This project is provided as-is for educational and development purposes.