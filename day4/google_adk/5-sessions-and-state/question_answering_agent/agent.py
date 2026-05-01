import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
# Load environment variables from the .env file in this directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# https://docs.litellm.ai/docs/providers/groq
model = LiteLlm(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)

# Create the root agent
question_answering_agent = Agent(
    name="question_answering_agent",
    #model="gemini-2.0-flash",
    model=model,
    description="Question answering agent",
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
)
