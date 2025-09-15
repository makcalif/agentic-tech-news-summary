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
    llm_config = {
        "model": "gpt-4.1-nano",
        # "request_timeout": 120,
    }

    web_browser = WebBrowser(max_content_length=30000, timeout=15)

    def generate_reply(self, messages, sender, **kwargs):
        last_message = messages[-1]["content"] if messages else ""
        
        # This only triggers if URL is found
        if "techcrunch.com" in last_message or "browse" in last_message.lower():
            print('# ... web browsing logic')
            
        # If no URL found, it falls back to the parent class
        # But the parent class gets an empty message and generates the error
        return super().generate_reply(messages, sender, **kwargs)
    

    def web_browser_function(url: str) -> str:
        """Fetches and processes web page content for analysis."""
        print(f"Function called with URL: {url}")
        try:
            result = web_browser.fetch_url(url)
            print(f"Function result length: {len(result)}")
            return result
        except Exception as e:
            return f"Error in web_browser_function: {str(e)}"
    
    # Create agent with function_map directly
    agent = autogen.ConversableAgent(
        name="TechNewsBrowserAgent",
        llm_config=llm_config,
        system_message="""You are an expert agentic AI news extractor. 

You have access to a function called 'web_browser_function' that can fetch web content.

When given a URL to browse:
1. Call web_browser_function with the URL
2. Analyze the returned content for agentic AI news
3. Return JSON format with headlines, excerpts, and URLs

Always use the web_browser_function when you need to fetch web content.""",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        function_map={"web_browser_function": web_browser_function}
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config={"use_docker": False},
        function_map={"web_browser_function": web_browser_function}
    )
    
    url = "https://techcrunch.com/category/artificial-intelligence/"
    task = f"""
Call web_browser_function("{url}") to fetch the content, then analyze it for agentic AI news.

Return JSON format:
[
    {{
        "headline": "title",
        "excerpt": "summary", 
        "url": "article_url"
    }}
]

Focus only on AI agents, multi-agent systems, and autonomous AI applications.
"""
    

    try:
        print("Starting chat...")
        result = user_proxy.initiate_chat(agent, message=task)
        print("Chat completed!")
        return result
    except Exception as e:
        print(f"Error during chat: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()