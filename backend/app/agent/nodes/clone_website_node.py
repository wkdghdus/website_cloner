from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from agent.dto.cloning_output import Clone
from agent.prompts.clone_website_prompt import prompt
from agent.states.state import State
from constants.ai_models import LLM

llm = LLM()

def clone_website(state: State):

    try:
        print("Cloning:", state.given_url)

        # Construct the data URL for the base64 image
        image_data_url = f"data:image/jpeg;base64,{state.screen_shot}"

        # Define the messages
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": f"""
                    - HTML Content: {state.raw_html}
                    - Stylesheets: {state.stylesheets}
                    - Images: {state.images}
                    - Meta Tags: {state.meta}
                    - Font Info: {state.fonts}
                    Use this to reconstruct the website in a single HTML file with embedded CSS. Ensure the result matches the visual look and layout of the original as closely as possible.
                    """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data_url
                    }
                }
            ])
        ]

        # Create the prompt template
        base_prompt = ChatPromptTemplate.from_messages(messages)

        # Create the cloning chain
        cloning_chain = base_prompt | llm.with_structured_output(Clone)

        # Invoke the chain
        cloned_website = cloning_chain.invoke({})

        return {"cloned_website": cloned_website.html_output}
    except Exception as e:
        print("clone_website failed:", e)
        raise
