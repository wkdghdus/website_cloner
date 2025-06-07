"""Define a data enrichment agent.

Works with a chat model with tool calling support.
"""
from langgraph.graph import START
from langgraph.graph import StateGraph
from agent.states.state import State

from agent.nodes.clone_website_node import clone_website
from agent.nodes.scrape_website_node import web_scrape
from agent.nodes.reflection_node import reflection

# Create the graph
workflow = StateGraph(State)

# add nodes
workflow.add_node("scrape_website", web_scrape)
workflow.add_node("clone_website", clone_website)
workflow.add_node("reflection", reflection)

workflow.add_edge(START, "scrape_website")
workflow.add_edge("scrape_website", "clone_website")
workflow.add_edge("clone_website", "reflection")


graph = workflow.compile()

def get_clone(url: str) -> str:
    input_state = {"given_url": url, "cloned_website": None, "screen_shot": None}
    final_state = graph.invoke(input_state)

    html = final_state.get("cloned_website", "")

    print("Final HTML type:", type(html))
    print("Final HTML snippet:", str(html)[:200])

    if not isinstance(html, str):
        try:
            html = str(html)
        except Exception as e:
            print("Cannot convert HTML to string:", e)
            raise ValueError("Returned HTML is not a string.")

    return html
