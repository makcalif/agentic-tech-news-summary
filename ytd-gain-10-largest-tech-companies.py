import asyncio
import sys
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen import UserProxyAgent
from autogen import AssistantAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.messages import TextMessage, MultiModalMessage

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def extract_text_from_messages(messages):
    texts = []
    for m in messages:
        if isinstance(m, TextMessage):
            texts.append(m.content)
        elif isinstance(m, MultiModalMessage):
            # MultiModalMessage content is a list of items, extract text items only
            for item in m.content:
                if isinstance(item, str):
                    texts.append(item)
                else:
                    # Skip non-text multimodal content (e.g., images)
                    pass
        else:
            # Other message types can be ignored or handled if needed
            pass
    return "\n".join(texts)
 
# Instantiate the model client (use "gpt-4o" for multimodal capabilities)
model_client = OpenAIChatCompletionClient(model="gpt-4.1-nano")

# Define the MultimodalWebSurfer agent
web_surfer_agent = MultimodalWebSurfer(
    name="MultimodalWebSurfer",
    model_client=model_client,
    debug_dir="./debug_data",
    to_save_screenshots=True,  # disables screenshot capture
    use_ocr=False,              # disables OCR/vision features
    animate_actions=False, 
)

# Create a simple AssistantAgent
assistant = AssistantAgent(
    name="simple_assistant",
    system_message="You are a helpful assistant.",
    llm_config={"config_list": [{"model": "gpt-4.1-nano"}]} 
)

# Create the UserProxyAgent
user_proxy = UserProxyAgent(
    name="user_proxy",
    # is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config={"use_docker": False},
    llm_config=False,  # Don't give this agent an LLM
)

# Example user query that requires browsing
 
 
def ytd_tech_companies():  
    user_proxy.initiate_chat(assistant, message="Show me the YTD gain of 10 largest technology companies as of today.")


# Main entry point (sync)
if __name__ == "__main__":
    ytd_tech_companies()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_main())
     