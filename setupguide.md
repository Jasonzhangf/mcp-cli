# MCP CLI System Configuration Guide

This guide outlines the steps to check your system configuration environment to ensure the MCP CLI operates correctly.

## 1. Python Environment

The MCP CLI requires Python 3.11 or newer.

**How to check:**
Open your terminal and run:
```bash
python3 --version
```
Ensure the output shows `Python 3.11.x` or higher. If not, you may need to install or update your Python version.

## 2. Virtual Environment and Dependencies

It is highly recommended to use a virtual environment to manage project dependencies. This project uses `uv` for dependency management.

**How to check/set up:**
1.  **Install `uv` (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    Or, if you have `pipx`:
    ```bash
    pipx install uv
    ```
2.  **Create and activate a virtual environment:**
    Navigate to the project root directory (`/Users/fanzhang/Documents/github/mcp-cli`) and run:
    ```bash
    uv venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    uv sync
    ```
    This will install all necessary packages listed in `pyproject.toml` and `uv.lock`.

## 3. Configuration Files

The MCP CLI relies on several configuration files.

*   **`server_config.json`**: Located in the project root, this file configures the MCP server connection.
    **How to check:** Verify its presence and content. A basic `server_config.json` might look like:
    ```json
    {
      "mcp_server_url": "http://localhost:8000"
    }
    ```
    Adjust `mcp_server_url` if your server is hosted elsewhere.

*   **`~/.chuk_llm/providers.yaml`**: This file configures your LLM providers (e.g., OpenAI, Anthropic).
    **How to check:**
    ```bash
    cat ~/.chuk_llm/providers.yaml
    ```
    Ensure your desired providers are configured correctly with their respective API keys (if applicable). Example for OpenAI:
    ```yaml
    openai:
      api_key: "sk-..."
      model: "gpt-4o"
    ```

*   **`~/.chuk_llm/.env`**: This file can store environment variables, including sensitive API keys.
    **How to check:**
    ```bash
    cat ~/.chuk_llm/.env
    ```
    Ensure any API keys or other sensitive environment variables are correctly set here.

## 4. Environment Variables

Some configurations, especially API keys, might be set via environment variables.

**How to check:**
You can check specific environment variables using `echo`:
```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
# etc.
```
Ensure these variables are set if your `providers.yaml` or other configurations rely on them.

## 5. Network Connectivity

The MCP CLI communicates with an MCP server and potentially external LLM provider APIs.

**How to check:**
1.  **MCP Server Connectivity:**
    If your `mcp_server_url` is `http://localhost:8000`, ensure your MCP server is running. You can try to `ping` it (though `ping` might not work for HTTP services, it's a quick check for host reachability):
    ```bash
    ping localhost
    ```
    A more direct check would be to use `curl` on the server's health endpoint if available, or simply try running an MCP CLI command that connects to the server.

2.  **LLM Provider API Connectivity:**
    Ensure you have internet access and that there are no firewall rules blocking access to LLM provider endpoints (e.g., `api.openai.com`, `api.anthropic.com`).

## 6. Running Diagnostics

The project includes diagnostic scripts that can help verify the setup.

**How to run:**
Navigate to the `diagnostics/` directory and run relevant scripts. For example:
```bash
cd diagnostics/
python3 provider_list_diagnostic.py
python3 mcp_server_diagnostic.py
```
These scripts can provide insights into your LLM provider and MCP server configurations.
