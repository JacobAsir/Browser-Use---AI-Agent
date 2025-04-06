import os
import sys
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent
from concurrent.futures import ThreadPoolExecutor

# Set event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Streamlit app
st.title("AI Agent Automation")
st.write("""
This app uses Browser Use to connect AI agents with the browser, enabling them to perform automated tasks and gather information from the web.
""")

# User input for the task
task = st.text_area(
    "Enter your task",
    height=70,
)

# Function to run the task asynchronously
async def run_task(task_input):
    agent = Agent(
        task=task_input,
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    return result

# Thread pool executor to run async functions in a synchronous environment
def run_async_task(task_input):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(run_task(task_input))

# Button to trigger the task
if st.button("Run Task"):
    if task:
        st.write("The agent is working on your task...")
        
        # Run task asynchronously in a thread pool
        with ThreadPoolExecutor() as executor:
            result = executor.submit(run_async_task, task)
            st.write(f"Result: {result.result()}")
    else:
        st.error("Please enter a valid task.")
