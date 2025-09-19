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
query = """
Go to https://www.morningstar.com/funds/xnas/vfiax/quote.

1. Locate the "Key Stats" or "Fees & Expenses" section.
2. Read the **Adjusted Expense Ratio** (also called Net Expense Ratio).
3. Read the **Minimum Initial Investment**.
4. Return both values in JSON format with keys: 
   - 'expense_ratio'
   - 'min_investment'

Hints:
- Adjusted Expense Ratio is usually in a row labeled "Expense Ratio (Net)".
- Minimum Initial Investment is usually labeled "Minimum Investment" in the same section.
- Only return the numeric or monetary value (strip text like "USD").
"""

# Synchronous helper function
def process_summary(web_content):
    # Your extraction logic here
    web_summary = extract_text_from_messages(web_content.messages)
    return web_summary

# Async function where async calls live
async def async_main():
    try: 
        web_content = await web_surfer_agent.run(task=query) 
        web_summary = process_summary(web_content)
 
        chat_result = user_proxy.initiate_chat(
            assistant,
            message=f"Find Adj Expense Ratio and minimum investment and return in a json format along with fund name: {web_content}"
        )

        # The final message content is the last message in the chat history
        final_message = chat_result.chat_history[-1]
        final_output = final_message['content'].replace('TERMINATE', '').strip()

        print("\n--- Final Summary Output ---")
        print(final_output)
          
    except Exception as e:
        print(f"Caught an exception: {e}")
        web_content_error = "Default content or retry logic"
    finally:
        # This block will always run, whether an exception occurred or not
        print("Closing the web surfer agent.")
        await web_surfer_agent.close()

     

# Main entry point (sync)
if __name__ == "__main__":
    asyncio.run(async_main()) 
     