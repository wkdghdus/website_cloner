from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from agent.dto.reflection_output import Reflection
from agent.prompts.reflection_prompt import prompt
from agent.states.state import State
from langgraph.types import Command
from constants.ai_models import LLM

import base64
import threading
import uvicorn
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from playwright.sync_api import sync_playwright


def serve_html(html_string: str, port: int = None):
    app = FastAPI()

    if port is None:
        port = random.randint(10000, 60000)

    @app.get("/")
    async def root():
        return HTMLResponse(content=html_string)
    

    def run():
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{port}/"


def screenshot_as_base64(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        buffer = page.screenshot(full_page=True)
        browser.close()
    return base64.b64encode(buffer).decode("utf-8")


llm = LLM()

def reflection(state: State) -> Command[Literal["clone_website", "__end__"]]:

    url = serve_html(state.cloned_website)
    cloned_base64 = screenshot_as_base64(url)
    

    try:
        print("Cloning:", state.given_url)

        # Construct the data URL for the base64 image
        initial_image_data_url = f"data:image/jpeg;base64,{state.screen_shot}"
        cloned_image_data_url = f"data:image/jpeg;base64,{cloned_base64}"


        # Define the messages
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": initial_image_data_url
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": cloned_image_data_url
                    }
                }
            ])
        ]

        # Create the prompt template
        base_prompt = ChatPromptTemplate.from_messages(messages)

        # Create the cloning chain
        reflection_chain = base_prompt | llm.with_structured_output(Reflection)

        # Invoke the chain
        reflection = reflection_chain.invoke({})


        print("reflection result: ", reflection.similarity_result)

        if reflection.similarity_result == True:
            return Command(goto="__end__")
        else:
            return Command(goto="clone_website")

    except Exception as e:
        print("clone_website failed:", e)
        raise
