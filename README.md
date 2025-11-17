# Anomaly Detection LangGraph Agent with Streamlit UI

A fully local anomaly detection agent built with LangGraph and powered by OpenAI's GPT-4o-mini, featuring a user-friendly Streamlit interface.

## 🌟 Features

- **Fully Local Execution**: No LangGraph Studio needed - runs completely on your machine
- **Interactive UI**: Beautiful Streamlit interface for easy interaction
- **Intelligent Analysis**: Uses LangGraph + OpenAI LLM + Pandas Agent for smart anomaly detection
- **Flexible Data Input**: Upload your own CSV or use the default dataset
- **Real-time Results**: See the agent's workflow and analysis in real-time
- **Multi-view Dashboard**: Analysis results, workflow steps, and data preview in organized tabs

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# 1. Run the setup script (uses UV for fast dependency management)
./setup.sh

# 2. Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 3. Run the app
./run.sh
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment with UV
uv venv
source .venv/bin/activate

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 4. Run the Streamlit app
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

> **Note**: This project uses [UV](https://github.com/astral-sh/uv) for fast Python package management. If you don't have UV installed, get it here: https://astral.sh/uv

## 🎯 Usage

### Using the UI

1. **Select Data Source**:

   - Choose "Use Default Dataset" to use the included sample data
   - Choose "Upload CSV File" to analyze your own data

2. **Run Analysis**:

   - Click the "🚀 Run Analysis" button in the sidebar

3. **View Results**:
   - **Analysis Results** tab: See the AI-powered anomaly detection results
   - **Agent Workflow** tab: Understand how the agent processed your request
   - **Data Preview** tab: Explore your dataset and statistics

### Using the Command Line (Optional)

You can still run the agent without the UI:

```bash
python test_agent.py
```

## 📊 Metrics Analyzed

The agent analyzes the following system metrics:

- `system.memory.used.percent` - Memory usage percentage
- `system.cpu.percent` - CPU usage percentage
- `system.network.tcp.connections` - TCP connection count

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LangGraph      │
│  State Graph    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│  Load  │ │ Analyze  │
│  Data  │ │ w/ Agent │
└────────┘ └──────────┘
              │
              ▼
        ┌──────────┐
        │ GPT-4o   │
        │   Mini   │
        └──────────┘
```

## 📁 Project Structure

```
anomaly-detection-langgraph-agent/
├── app.py                          # Streamlit UI (NEW!)
├── agent/
│   ├── agent.py                    # LangGraph workflow definition
│   ├── data/
│   │   └── merged_metrics(in).csv  # Sample dataset
│   └── utils/
│       ├── nodes.py                # Agent node functions
│       └── state.py                # State definition
├── test_agent.py                   # CLI test script
├── requirements.txt                # Python dependencies
├── langgraph.json                  # LangGraph config (not needed for local)
└── README.md                       # This file
```

## 🔧 Configuration

### Streamlit Configuration

You can customize the Streamlit app by creating a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
```

### Agent Configuration

The agent uses GPT-4o-mini by default. To use a different model, edit `agent/utils/nodes.py`:

```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # Change to gpt-4 or other models
```

## 🆚 Differences from LangGraph Studio

| Feature           | LangGraph Studio             | This App (Streamlit)            |
| ----------------- | ---------------------------- | ------------------------------- |
| **Deployment**    | Cloud-based                  | Fully Local                     |
| **UI**            | LangSmith UI                 | Streamlit UI                    |
| **Setup**         | Requires LangSmith account   | Just run `streamlit run app.py` |
| **Cost**          | Subscription may be required | Free (only OpenAI API costs)    |
| **Customization** | Limited                      | Full control over UI            |
| **Data Privacy**  | Data sent to LangSmith       | Data stays local                |

## 💡 Tips

- **File Size**: For large CSV files, consider sampling or filtering data before analysis
- **API Costs**: GPT-4o-mini is cost-effective, but monitor your OpenAI usage
- **Custom Metrics**: Modify `agent/utils/nodes.py` to analyze different metrics
- **Error Handling**: Check the error messages in the UI for troubleshooting

## 🐛 Troubleshooting

### "Module not found" Error

```bash
pip install -r requirements.txt
```

### "OpenAI API Key not found"

Make sure you have created a `.env` file with your OpenAI API key.

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this project!

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- UI powered by [Streamlit](https://streamlit.io/)
- AI capabilities from [OpenAI](https://openai.com/)
