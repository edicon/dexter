# Dexter - Autonomous Financial Research Agent

Dexter is an AI agent designed for autonomous financial research, capable of analyzing complex financial questions, planning tasks, self-reflecting, and utilizing real-time market data to provide comprehensive answers.

## Overview

Dexter breaks down complex queries into structured research steps, executes these steps using various financial data tools, validates its own work, and refines results to deliver data-backed insights.

**Key Capabilities:**
*   **Intelligent Task Planning**: Decomposes complex queries into actionable research steps.
*   **Autonomous Execution**: Selects and runs appropriate tools to gather financial data.
*   **Self-Validation**: Checks its own progress and iterates on tasks until completion.
*   **Real-Time Financial Data**: Accesses income statements, balance sheets, cash flow statements, stock prices, crypto prices, news, and more.
*   **Safety Features**: Includes built-in loop detection and step limits to prevent runaway execution.

**Architecture:**
Dexter employs a multi-agent architecture with specialized components:
*   **Planning Agent**: Analyzes queries and generates structured task lists.
*   **Action Agent**: Selects and executes the necessary tools for research steps.
*   **Validation Agent**: Verifies task completion and data sufficiency.
*   **Answer Agent**: Synthesizes findings into comprehensive, data-rich responses.

**Technologies:**
*   Python 3.10 or higher
*   `uv` package manager
*   LangChain for orchestrating LLM interactions and agents.
*   OpenAI for large language models (defaulting to `gpt-4.1`).
*   Pydantic for data validation and schema definition.
*   `python-dotenv` for environment variable management.

## Building and Running

### Prerequisites
*   Python 3.10 or higher
*   `uv` package manager (installation: `pip install uv`)
*   An OpenAI API key (available [here](https://platform.openai.com/api-keys)).
*   A Financial Datasets API key (available [here](https://financialdatasets.ai)).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/virattt/dexter.git
    cd dexter
    ```

2.  **Install dependencies with `uv`:**
    ```bash
    uv sync
    ```

3.  **Set up your environment variables:**
    Copy `env.example` to `.env` and populate it with your API keys.
    ```bash
    cp env.example .env
    ```
    Edit `.env` to include:
    ```
    OPENAI_API_KEY=your-openai-api-key
    FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

    # Optional: LangSmith for tracing and debugging
    # LANGSMITH_API_KEY=your-langsmith-api-key
    # LANGSMITH_ENDPOINT=https://api.smith.langchain.com
    # LANGSMITH_PROJECT=dexter
    # LANGSMITH_TRACING=true
    ```

### Usage

Run Dexter in interactive mode:
```bash
uv run dexter-agent
```
You can then ask Dexter financial questions directly in the terminal.

## Development Conventions

### Code Structure
The core logic resides in the `src/dexter/` directory, organized as follows:
*   `agent.py`: Main agent orchestration logic.
*   `cli.py`: Command-line interface entry point.
*   `model.py`: Abstraction layer for LLM calls.
*   `prompts.py`: System prompts used by various agents.
*   `schemas.py`: Pydantic models for data validation and structured outputs.
*   `tools/`: Directory containing all available tools, categorized by domain (e.g., `finance`, `crypto`, `search`).
*   `utils/`: General utility functions (e.g., logging, UI, context management).

### LLM Interaction
Dexter interacts with Large Language Models (LLMs) primarily through `langchain_openai.ChatOpenAI`, defaulting to `gpt-4.1`. It uses `ChatPromptTemplate` for consistent prompt formatting and supports structured output and tool calling. Streaming responses are utilized for generating final answers.

### Available Tools
Dexter comes equipped with a rich set of tools to access various data sources:
*   **Financial Filings**: `get_filings`, `get_10K_filing_items`, `get_10Q_filing_items`, `get_8K_filing_items`.
*   **Financial Fundamentals**: `get_income_statements`, `get_balance_sheets`, `get_cash_flow_statements`, `get_all_financial_statements`.
*   **Financial Metrics**: `get_financial_metrics_snapshot`, `get_financial_metrics`.
*   **Financial Prices**: `get_price_snapshot`, `get_prices`.
*   **News**: `get_news`.
*   **Estimates**: `get_analyst_estimates`.
*   **Segments**: `get_segmented_revenues`.
*   **Search**: `search_google_news`.
*   **Crypto**: `get_crypto_price_snapshot`, `get_crypto_prices`.

### Configuration
Agent behavior can be configured within the `Agent` class initialization, allowing adjustment of global and per-task step limits:
```python
agent = Agent(
    max_steps=20,              # Global safety limit
    max_steps_per_task=5       # Per-task iteration limit
)
```

### Logging and Tracing
Dexter integrates custom logging via `dexter.utils.logger` and supports optional tracing and debugging through LangSmith, configured via environment variables.

## License
This project is licensed under the MIT License.
