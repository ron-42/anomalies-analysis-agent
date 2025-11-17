"""State definition for the anomaly detection agent"""

from typing import TypedDict, Annotated
import pandas as pd
from langgraph.graph.message import add_messages


class State(TypedDict):
    """Agent state for anomaly detection workflow"""

    messages: Annotated[list, add_messages]
    csv_path: str  # Path to CSV file
    df: pd.DataFrame  # Loaded dataframe
