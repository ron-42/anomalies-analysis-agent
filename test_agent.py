"""Minimal smart agent test with LLM analysis"""

from agent.agent import graph
from langchain_core.messages import HumanMessage
from langfuse.callback import CallbackHandler


def main():
    """Run the anomaly detection agent"""
    print("\n" + "=" * 60)
    print("🤖 Smart Anomaly Detection Agent with Langfuse Tracing")
    print("=" * 60 + "\n")

    # Initialize Langfuse callback
    langfuse_handler = CallbackHandler()

    # Initialize state
    initial_state = {
        "messages": [HumanMessage(content="Analyze data for anomalies")],
        "csv_path": "",
        "df": None,
    }

    # Run the graph with Langfuse tracing
    result = graph.invoke(initial_state, config={"callbacks": [langfuse_handler]})

    # Print minimal output - only key messages
    for msg in result["messages"]:
        if hasattr(msg, "content"):
            # Skip the initial human message
            if not isinstance(msg, HumanMessage):
                print(msg.content)
                print()

    # Flush Langfuse to ensure all traces are sent
    langfuse_handler.flush()
    print("\n✓ Traces sent to Langfuse at http://localhost:3000")


if __name__ == "__main__":
    main()
