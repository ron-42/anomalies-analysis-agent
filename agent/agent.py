"""Main agent graph construction for anomaly detection"""

from langgraph.graph import StateGraph, START, END
from agent.utils.state import State
from agent.utils.nodes import load_data_node, analyze_with_pandas_agent_node


# Define a new graph
workflow = StateGraph(State)

# Add nodes - simplified to 2 nodes using pandas agent
workflow.add_node("load_data", load_data_node)
workflow.add_node("analyze", analyze_with_pandas_agent_node)

# Set the entrypoint as `load_data`
# This means that this node is the first one called
workflow.add_edge(START, "load_data")

# Add edge from load_data to analyze
# This means that after `load_data` is called, `analyze` node is called next
workflow.add_edge("load_data", "analyze")

# Add edge from analyze to END
# This marks the end of the graph
workflow.add_edge("analyze", END)

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()
