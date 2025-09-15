# Agentic Tech News Summary

This project provides an agentic pipeline for automatically browsing, extracting, and summarizing the latest news about agentic AI from TechCrunch, and identifying tools/frameworks mentioned in those articles.

## Features
- **Web Browser Tool**: Fetches and returns HTML content from a given URL for LLM analysis.
- **TechNewsBrowserAgent**: Uses LLM to extract and summarize agentic AI news from TechCrunch's AI section.
- **ToolFinderAgent**: Uses LLM to analyze article text and extract any mentioned agentic AI tools/frameworks (e.g., n8n, LangChain, CrewAI, etc.).

## Usage
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY=sk-...
   ```
3. **Run the main pipeline**
   - Example:
     ```bash
     python technews_agent.py
     

## File Structure
- `technews_agent.py` — Main agent for browsing and summarizing TechCrunch AI news.
- `tech2.py` — Example pipeline using function-calling for web browsing and tool extraction.
- `web_browser_tool.py` — Contains the `WebBrowserTool` class for fetching web content.
- `tool_finder_agent.py` — Contains the `ToolFinderAgent` class for extracting tool mentions from article text.
- `requirements.txt` — Python dependencies.

## Customization
- You can extend the `WebBrowserTool` to add more advanced scraping or parsing logic.
- The LLM prompts can be customized for different news sources or extraction criteria.


pip list --format=freeze > requirements.txt
