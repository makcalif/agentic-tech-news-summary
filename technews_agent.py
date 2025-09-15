import os
import autogen
from autogen.tools import Tool
from web_browser_tool import WebBrowser

# Try these imports one by one:
try:
    from autogen.tools import tool
except ImportError:
    try:
        from autogen import tool
    except ImportError:
        print("tool decorator not found, using register_function approach instead")
        tool = None

def main():
    # Create an LLM agent with browsing tool enabled
    llm_config = {
        "model": "gpt-4.1-nano",
        # "request_timeout": 120,
    }

    web_browser = WebBrowser(max_content_length=30000, timeout=15)

    def web_browser_function(url: str) -> str:
            """
            Fetches and processes web page content, removing HTML tags but preserving text structure for LLM analysis.
            
            Args:
                url: The URL of the web page to fetch
                
            Returns:
                str: Processed content from the web page
            """
            return web_browser.fetch_url(url)

    # web_browser_tool = Tool(
    #     name="web_browser",
    #     description="Fetches and processes web page content, removing HTML tags but preserving text structure for LLM analysis.",
    #     func=web_browser.fetch_url
    # )
    
        # Use the @tool decorator to create the tool
    # @tool
    # def web_browser_tool(url: str) -> str:
    #     """
    #     Fetches and processes web page content, removing HTML tags but preserving text structure for LLM analysis.
        
    #     Args:
    #         url: The URL of the web page to fetch
            
    #     Returns:
    #         str: Processed content from the web page
    #     """
    #     return web_browser.fetch_url(url)
    
     # Create agent WITHOUT tools parameter
    agent = autogen.AssistantAgent(
        name="TechNewsBrowserAgent",
        llm_config=llm_config,
        system_message="""You are an expert agentic AI news extractor. You have access to a web_browser_function that can fetch content from websites. 

When given a URL:
1. Use the web_browser_function to fetch the content
2. Analyze the content to extract relevant information about AGENTIC AI only
3. Focus on finding article titles, content, publication dates, and other news-related information
4. Return ONLY valid JSON output as requested - no explanations, no markdown, just pure JSON

You are skilled at reading and understanding web content to extract meaningful information about AI agents, multi-agent systems, and autonomous AI applications.""",
    )


     # Register the function with the agent AFTER creating the agent
    autogen.register_function(
        web_browser_function,
        caller=agent,
        executor=agent,
        name="web_browser_function",
        description="Fetches and processes web page content for analysis"
    )

#     agent = autogen.AssistantAgent(
#         name="TechNewsBrowserAgent",
#         llm_config=llm_config,
#         system_message="""You are an expert agentic AI news extractor. You have access to a web browser tool that can fetch content from websites. 

# When given a URL:
# 1. Use the web_browser tool to fetch the content
# 2. Analyze the content to extract relevant information
# 3. Focus on finding article titles, content, publication dates, and other news-related information
# 4. Return only the required JSON output as requested by the user

# You are skilled at reading and understanding web content to extract meaningful information.""",
#     # code_execution_config={"use_docker": False},
#     tools=[web_browser_tool]  # or [web_browser_raw_tool] for raw HTML
        
        
        # system_message="You are an expert agentic AI news extractor. You strictly follow the user's prompt and return only the required JSON output.",
        # code_execution_config={"use_docker": False},
        # tools=[web_browser_tool]
        # func=web_browser.get_raw_html
    # )




    url = "https://techcrunch.com/category/artificial-intelligence/"
    task = f"""
Please browse this website and extract agentic AI news articles: {url}

Use the web_browser_function to fetch the content first, then analyze it.

Requirements:
1. Focus **only on agentic AI news** (AI agents, multi-agent systems, autonomous AI applications)
2. For each relevant article, capture:
   - **headline**: the title of the article
   - **excerpt**: a short summary or first 2-3 sentences
   - **url**: direct link to the article

3. Return ONLY valid JSON in this exact format:
[
    {{
        "headline": "Example headline",
        "excerpt": "Short summary of the article.",
        "url": "https://link-to-article.com"
    }}
]

4. Exclude non-agentic AI topics (theoretical papers, AI ethics, AI art, etc.)
5. Return only the JSON array - no other text or formatting.
"""
    
    
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
    )
    url = "https://techcrunch.com/category/artificial-intelligence/"
    task = f"""
1. Focus **only on agentic AI news**. Ignore unrelated AI topics (like purely theoretical AI papers, AI ethics without agentic application, or AI art).  
2. For each relevant article, capture:
     - **Headline**: the title of the article.
     - **Excerpt**: a short summary or first 2–3 sentences that describe the news.
     - **URL**: link to the article.

3. Present your output in **JSON format** like this:

[
    {{
        "headline": "Example headline",
        "excerpt": "Short summary or first few sentences of the article.",
        "url": "https://link-to-article.com"
    }}
]

4. Only include **articles that describe agentic AI systems, multi-agent frameworks, autonomous AI applications, or AI agents performing tasks**. Skip other AI news.

Website to scan: {url}

Return the JSON output only. No extra commentary.
"""
    
   
    try:
        result = user_proxy.initiate_chat(agent, message=task)
        print("Chat completed successfully!")
        return result
    except Exception as e:
        print(f"Error during chat: {e}")
        return None
if __name__ == "__main__":
    main()
