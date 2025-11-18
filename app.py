"""Streamlit UI for Anomaly Detection LangGraph Agent"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
from agent.agent import graph

# Initialize Phoenix tracing
import phoenix as px
from phoenix.otel import register

# Launch Phoenix and setup tracing
if "phoenix_initialized" not in st.session_state:
    # Set environment variables for Phoenix configuration
    os.environ["PHOENIX_PORT"] = "6007"  # Phoenix UI port
    os.environ["PHOENIX_HOST"] = "0.0.0.0"  # Allow external access
    os.environ["PHOENIX_GRPC_PORT"] = (
        "4318"  # Use custom gRPC port (avoid 4317 conflicts)
    )

    # Launch Phoenix UI
    st.session_state.phoenix_session = px.launch_app()

    # Register tracer with auto-instrumentation
    # Phoenix will use gRPC on port 4318 for better performance
    tracer_provider = register(
        project_name="anomaly-detection-agent",
        auto_instrument=True,  # Auto-instrument LangChain
    )

    st.session_state.phoenix_initialized = True

# Page configuration
st.set_page_config(
    page_title="Anomaly Detection Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background-color: #f0f2f6;
        color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .step-box h3 {
        color: #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    .analysis-box {
        background-color: #e7f3ff;
        color: #004085;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #1f77b4;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "result" not in st.session_state:
    st.session_state.result = None
if "csv_path" not in st.session_state:
    st.session_state.csv_path = None

# Main header
st.markdown(
    '<div class="main-header">🔍 Anomaly Detection Agent</div>', unsafe_allow_html=True
)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # Data source selection
    data_source = st.radio(
        "Select Data Source:",
        ["Use Default Dataset", "Upload CSV File"],
        help="Choose to use the default dataset or upload your own",
    )

    csv_path = None
    uploaded_file = None

    if data_source == "Upload CSV File":
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=["csv"],
            help="Upload a CSV file with system metrics",
        )
        if uploaded_file:
            # Save uploaded file temporarily
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            csv_path = temp_path
            st.success(f"✓ File uploaded: {uploaded_file.name}")
    else:
        # Use default dataset
        default_path = os.path.join(
            os.path.dirname(__file__), "agent", "data", "merged_metrics(in).csv"
        )
        if os.path.exists(default_path):
            csv_path = default_path
            st.info(f"📁 Using default dataset: merged_metrics(in).csv")
        else:
            st.error("❌ Default dataset not found!")

    st.markdown("---")

    # Analysis button
    analyze_button = st.button(
        "🚀 Run Analysis",
        type="primary",
        disabled=(csv_path is None),
    )

    st.markdown("---")

    # Info section
    st.header("ℹ️ About")
    st.markdown("""
    This agent analyzes system metrics to detect anomalies using:
    
    - **LangGraph**: Orchestrates the workflow
    - **OpenAI GPT-4o-mini**: Powers intelligent analysis
    - **Pandas Agent**: Performs data analysis
    
    **Metrics analyzed:**
    - Memory usage %
    - CPU usage %
    - TCP connections
    """)

    st.markdown("---")

    # Phoenix Tracing section
    st.header("🔍 Phoenix Tracing")
    st.info("Phoenix is running at http://localhost:6007")
    if st.button("📊 Open Phoenix UI", key="phoenix_btn"):
        st.markdown(
            "[Click here to open Phoenix](http://localhost:6007)",
            unsafe_allow_html=True,
        )

    # Reset button
    if st.button("🔄 Reset"):
        st.session_state.analysis_done = False
        st.session_state.result = None
        st.session_state.csv_path = None
        st.rerun()

# Main content area
if analyze_button and csv_path:
    st.session_state.csv_path = csv_path

    # Create progress indicators
    with st.spinner("🔄 Running anomaly detection agent..."):
        try:
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content="Analyze data for anomalies")],
                "csv_path": csv_path,
                "df": None,
            }

            # Run the graph
            result = graph.invoke(initial_state)

            st.session_state.result = result
            st.session_state.analysis_done = True

        except Exception as e:
            st.error(f"❌ Error running analysis: {str(e)}")
            st.exception(e)

# Display results
if st.session_state.analysis_done and st.session_state.result:
    result = st.session_state.result

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["📊 Analysis Results", "📋 Agent Workflow", "📈 Data Preview"]
    )

    with tab1:
        st.header("Analysis Results")

        # Display all messages from the agent
        for i, msg in enumerate(result["messages"]):
            if hasattr(msg, "content") and not isinstance(msg, HumanMessage):
                content = msg.content

                # Check message type and display accordingly
                if "✓" in content:
                    st.markdown(
                        f'<div class="success-box">{content}</div>',
                        unsafe_allow_html=True,
                    )
                elif "✗" in content:
                    st.markdown(
                        f'<div class="error-box">{content}</div>',
                        unsafe_allow_html=True,
                    )
                elif "🤖" in content or "LLM Analysis" in content:
                    st.markdown(
                        f'<div class="analysis-box">{content}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="step-box">{content}</div>', unsafe_allow_html=True
                    )

    with tab2:
        st.header("Agent Workflow")

        # Display workflow steps
        st.markdown("""
        The agent follows these steps:
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
            <div class="step-box">
                <h3>1️⃣ Load Data</h3>
                <p>Load and validate CSV data</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class="step-box">
                <h3>2️⃣ Analyze</h3>
                <p>Use LLM + Pandas Agent to detect anomalies</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
            <div class="step-box">
                <h3>3️⃣ Report</h3>
                <p>Generate actionable insights</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Display message history
        st.subheader("Message History")
        for i, msg in enumerate(result["messages"]):
            if hasattr(msg, "content"):
                msg_type = "Human" if isinstance(msg, HumanMessage) else "AI"
                with st.expander(f"Message {i + 1} ({msg_type})", expanded=(i == 0)):
                    st.write(msg.content)

    with tab3:
        st.header("Data Preview")

        if result.get("df") is not None:
            df = result["df"]

            # Display basic stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("CSV Path", Path(st.session_state.csv_path).name)

            # Display dataframe
            st.subheader("Dataset Preview")
            st.dataframe(df.head(100), width="stretch")

            # Display column info
            st.subheader("Column Information")
            col_info = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str).values,
                    "Non-Null Count": df.count().values,
                    "Null Count": df.isnull().sum().values,
                }
            )
            st.dataframe(col_info, width="stretch")

            # Display basic statistics for numeric columns
            st.subheader("Numeric Statistics")
            numeric_df = df.select_dtypes(include=["float64", "int64"])
            if not numeric_df.empty:
                st.dataframe(numeric_df.describe(), width="stretch")
        else:
            st.warning("No data available to preview")

# Initial state display
if not st.session_state.analysis_done:
    st.info(
        "👈 Configure your data source in the sidebar and click 'Run Analysis' to start detecting anomalies!"
    )

    # Show example/default data if available
    default_path = os.path.join(
        os.path.dirname(__file__), "agent", "data", "merged_metrics(in).csv"
    )

    if os.path.exists(default_path):
        with st.expander("📊 Preview Default Dataset", expanded=False):
            try:
                df_preview = pd.read_csv(default_path)
                st.write(
                    f"**Records:** {len(df_preview)} | **Columns:** {len(df_preview.columns)}"
                )
                st.dataframe(df_preview.head(10), width="stretch")
            except Exception as e:
                st.error(f"Could not preview default dataset: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with ❤️ using LangGraph + Streamlit | Fully Local Execution
</div>
""",
    unsafe_allow_html=True,
)
