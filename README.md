<div align="center">

# Keyword Extractor Ai MCP

**MCP server for keyword extractor ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-keyword-extractor-ai-mcp)](https://pypi.org/project/meok-keyword-extractor-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Keyword Extractor Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `extract_keywords` | Extract top keywords using TF-IDF scoring with stop word filtering and frequency |
| `analyze_density` | Calculate keyword density for SEO analysis, with target keyword tracking and rec |
| `suggest_tags` | Suggest tags and categories for content based on keyword analysis and topic matc |
| `compare_keywords` | Compare keywords between two texts to find common, unique, and differentiating t |

## Installation

```bash
pip install meok-keyword-extractor-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "keyword-extractor-ai": {
      "command": "python",
      "args": ["-m", "meok_keyword_extractor_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
