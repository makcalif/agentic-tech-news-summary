
# Agentic Tech News Summary

This project provides agentic pipelines for browsing, extracting, and summarizing tech news, financial data, and index fund information using LLMs and browser automation.

## Features

- **TechCrunch AI News Extraction**: Browse and summarize agentic AI news from TechCrunch using multimodal agents and Playwright automation.
- **Tool Extraction**: Identify agentic AI tools/frameworks (e.g., n8n, LangChain, CrewAI) mentioned in articles.
- **Financial Data Extraction**: Scripts for YTD gain of top tech companies and index fund analysis using LLMs and web browsing.
- **Reddit & Morningstar Index Fund Analysis**: Extract mutual fund tickers from Reddit and fetch financial stats from Morningstar.
- **MCP Server Integration**: Use MCP server and Playwright for robust browser automation.

## Usage

1. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    python -m playwright install
    ```

2. **Set your OpenAI API key**
    ```bash
    export OPENAI_API_KEY=sk-...
    ```

3. **Run the main agents/scripts**
    - TechCrunch AI news:  
       `python techcrunch-ai-news.py`
    - YTD gain for tech companies:  
       `python ytd-gain-10-largest-tech-companies.py`
    - Reddit index fund analysis:  
       `python redditIndexFund1.py`
    - Single index fund analysis:  
       `python singleIndexFund.py`
    - MCP Playwright browser agent:  
       `python mcp_playwright_agent.py`
    - Start MCP server (if needed):  
       `python mcpServer.py`

## File Structure

- `techcrunch-ai-news.py` — Multimodal agent for TechCrunch AI news.
- `ytd-gain-10-largest-tech-companies.py` — YTD gain extraction for top tech companies.
- `redditIndexFund1.py` — Reddit index fund ticker and Morningstar stats extraction.
- `singleIndexFund.py` — Single index fund stats extraction from Morningstar.
- `technews_agent.py`, `tech2.py` — Legacy/experimental agentic pipelines.
- `web_browser_tool.py` — Web browser tool for HTML fetching.
- `tool_finder_agent.py` — Agent for extracting tool mentions from text.
- `mcp_playwright_agent.py` — MCP Playwright browser agent.
- `mcpServer.py` — MCP server startup script.
- `requirements.txt` — Python dependencies.
- `debug_data/` — Debug output directory.

## Customization

- Extend agents or tools for new sources, financial data, or custom extraction logic.
- Adjust prompts and agent configs for different LLMs or browsing strategies.

## Troubleshooting

- Ensure MCP server is running before using MCP-based agents.
- If browser automation fails, check Playwright installation and MCP server logs.
- For LLM errors, verify your OpenAI API key and model availability.

## License

MIT
