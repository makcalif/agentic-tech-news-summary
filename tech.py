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
    
    # Custom agent that handles web browsing internally
    class WebBrowsingAgent(autogen.AssistantAgent):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.web_browser = web_browser
        
        def generate_reply(self, messages, sender, **kwargs):
            # Check if the message contains a URL to browse
            last_message = messages[-1]["content"] if messages else ""
            
            if "browse" in last_message.lower() or "http" in last_message:
                # Extract URL from message
                import re
                urls = re.findall(r'https?://[^\s]+', last_message)
                if urls:
                    url = urls[0]
                    print(f"Browsing URL: {url}")
                    web_content = self.web_browser.fetch_url(url)
                    
                    # Add the web content to the message context
                    enhanced_message = f"{last_message}\n\nWEB CONTENT:\n{web_content}"
                    
                    # Create new messages list with enhanced content
                    new_messages = messages[:-1] + [{"role": "user", "content": enhanced_message}]
                    return super().generate_reply(new_messages, sender, **kwargs)
            
            return super().generate_reply(messages, sender, **kwargs)
    
    agent = WebBrowsingAgent(
        name="TechNewsBrowserAgent",
        llm_config=llm_config,
        system_message="""You are an expert agentic AI news extractor. When you receive web content, analyze it to extract agentic AI news and return JSON format.""",
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config=False,
    )
    
    url = "https://techcrunch.com/category/artificial-intelligence/"
    task = f"Please browse {url} and extract agentic AI news in JSON format."
    
    try:
        result = user_proxy.initiate_chat(agent, message=task)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    main()
