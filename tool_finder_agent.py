import autogen

class ToolFinderAgent:
    def __init__(self, llm_config=None):
        self.llm_config = llm_config or {
            "model": "gpt-4.1-nano",
        }
        self.agent = autogen.ConversableAgent(
            name="ToolFinderAgent",
            llm_config=self.llm_config,
            system_message="You are an expert at reading AI news articles and identifying any tools, frameworks, or platforms used in agentic AI (such as n8n, LangChain, AutoGen, CrewAI, etc). When given article text, return a JSON list of all tools/frameworks/platforms mentioned, with a short description for each. Return only the JSON list, no extra commentary.",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
        )

    def find_tools(self, article_text):
        prompt = f"""
Read the following article text and extract the names of any tools, frameworks, or platforms used in agentic AI (e.g., n8n, LangChain, AutoGen, CrewAI, etc). For each, provide a short description. Return only a JSON list like this:
[
  {{
    "tool": "ToolName",
    "description": "Short description of the tool/framework/platform."
  }}
]

Article text:
{article_text}
"""
        return self.agent.generate_reply([
            {"role": "user", "content": prompt}
        ], sender="User")
