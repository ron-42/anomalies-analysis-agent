"""Simplified node functions using pandas dataframe agent"""

import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from .state import State

# Load environment variables
load_dotenv()


def load_data_node(state: State) -> State:
    """Load CSV data into DataFrame"""
    try:
        # Check if csv_path is provided in state, otherwise use default
        csv_path = state.get("csv_path", "")

        # If no csv_path provided or empty, use default path
        if not csv_path or csv_path.strip() == "":
            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data",
                "merged_metrics(in).csv",
            )

        df = pd.read_csv(csv_path)
        state["df"] = df
        state["csv_path"] = csv_path
        state["messages"].append(
            AIMessage(
                content=f"✓ Loaded {len(df)} records from {os.path.basename(csv_path)} with {len(df.columns)} metrics"
            )
        )
    except Exception as e:
        state["messages"].append(AIMessage(content=f"✗ Error loading data: {str(e)}"))

    return state


def analyze_with_pandas_agent_node(state: State) -> State:
    """Use pandas dataframe agent to analyze and detect anomalies with LLM"""
    df = state.get("df")

    if df is None or df.empty:
        state["messages"].append(AIMessage(content="✗ No data available"))
        return state

    try:
        # Create pandas dataframe agent with LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            agent_type="openai-tools",
            verbose=False,
            allow_dangerous_code=True,  # Required for pandas operations
        )

        # Ask the agent to detect and analyze anomalies
        # The agent will choose the best method on its own
        query = """Analyze this system metrics data for anomalies. 

Focus on these metrics:
- system.memory.used.percent
- system.cpu.percent  
- system.network.tcp.connections

Use any statistical or ML method you think is appropriate (you have full pandas and sklearn access).

Be brief and actionable.

this is referance output template and number may change:


The distribution ranges from 1 to 99 , a difference of 98
The average CPU Utilization(%) is 50.208
Maximum total CPU Utilization(%) of 99 was observed on 10 Nov 2025, 7:00 PM , whereas the minimum total CPU Utilization(%) of 1 was observed on 3 different hours
The total CPU Utilization(%) increased the most by 109.84% over the past 2 hours and dropped the most by 40.81% over the past 8 hours
Highest hour-over-hour increase in total CPU Utilization(%) was observed on 05 Nov 2025, 3:00 AM ( 6,700% ) whereas hour-over-hour total CPU Utilization(%) declined the most on 01 Nov 2025, 9:00 PM by 98.96%
Total CPU Utilization(%) remained above 74.604 throughout the period from 05 Nov 2025, 10:00 AM to 05 Nov 2025, 12:00 PM
Total CPU Utilization(%) remained below 25.604 throughout the period from 03 Nov 2025, 5:00 AM to 03 Nov 2025, 7:00 AM
"""

        # Run the agent
        response = agent.invoke({"input": query})
        analysis = response.get("output", "No analysis available")

        state["messages"].append(AIMessage(content=f"🤖 LLM Analysis:\n\n{analysis}"))

    except Exception as e:
        state["messages"].append(
            AIMessage(content=f"✗ Error during analysis: {str(e)}")
        )

    return state
