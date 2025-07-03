# 项目架构深度分析 (Project Architecture Deep Dive)

## 中文报告

### 1. 概述
MCP CLI（Model Context Protocol Command Line Interface）是一个功能丰富的命令行工具，旨在通过与Model Context Protocol服务器交互，实现与大型语言模型（LLMs）的无缝通信。它集成了CHUK Tool Processor和CHUK-LLM库，提供了工具使用、会话管理和多种操作模式。

### 2. 核心架构
MCP CLI采用模块化架构，职责分离清晰，主要由以下三个核心组件构成：
*   **CHUK Tool Processor**: 负责异步工具执行和与MCP服务器的通信。
*   **CHUK-LLM**: 提供统一的LLM提供商配置和客户端管理。
*   **MCP CLI (本项目)**: 提供丰富的用户界面和命令编排功能。

### 3. 主要功能与特性
*   **多种操作模式**:
    *   **聊天模式 (Chat Mode)**: 提供会话式界面，支持流式响应和自动化工具使用。
    *   **交互模式 (Interactive Mode)**: 命令驱动的Shell界面，用于直接服务器操作。
    *   **命令模式 (Command Mode)**: Unix友好模式，适用于脚本自动化和管道操作。
    *   **直接命令 (Direct Commands)**: 无需进入交互模式即可运行单个命令。
*   **高级聊天界面**: 支持流式响应、并发工具执行、智能中断、性能指标显示和富文本格式（Markdown渲染、语法高亮）。
*   **全面的提供商支持**: 支持OpenAI、Anthropic、Ollama以及自定义提供商，并支持会话中动态切换。
*   **强大的工具系统**: 自动发现服务器提供的工具、提供商适配、并发执行、丰富的进度显示、工具历史记录和流式工具调用。
*   **高级配置管理**: 支持通过环境变量、配置文件（`server_config.json`, `~/.chuk_llm/providers.yaml`, `~/.chuk_llm/.env`）进行配置，并提供用户偏好设置、验证和诊断功能。
*   **增强的用户体验**: 跨平台支持、丰富的控制台输出、命令自动补全、全面的帮助系统和优雅的错误处理。

### 4. 技术栈与依赖
*   **核心语言**: Python 3.11+
*   **LLM及MCP相关库**: `anthropic`, `google-genai`, `chuk-llm`, `chuk-mcp`, `chuk-tool-processor`
*   **CLI用户界面库**: `prompt-toolkit`, `rich`, `typer`
*   **核心工具库**: `asyncio` (异步编程), `python-dotenv` (环境变量管理)

### 5. 项目结构
项目结构清晰，主要源代码位于`src/mcp_cli/`目录下，并按功能模块划分：
*   `src/mcp_cli/chat/`: 聊天模式的核心逻辑，包括上下文、处理器、会话、UI和工具处理。
*   `src/mcp_cli/cli/`: 主CLI命令的注册和基础命令。
*   `src/mcp_cli/commands/`: 通用命令的实现。
*   `src/mcp_cli/interactive/`: 交互式Shell模式的逻辑。
*   `src/mcp_cli/llm/`: LLM客户端、系统提示生成和工具处理器。
*   `src/mcp_cli/tools/`: 工具适配器、格式化、管理器和模型定义。
*   `src/mcp_cli/ui/`: 用户界面辅助函数和颜色定义。
*   `src/mcp_cli/utils/`: 异步工具、LLM探测和Rich库辅助函数。
*   `src/mcp_cli/main.py`: `mcp-cli`的主入口点。
*   `tests/`: 包含与源代码结构对应的单元测试和集成测试。
*   `diagnostics/`: 诊断脚本。
*   `examples/`: 示例用法脚本。
*   `scripts/`: 包含`mcp-cli`可执行脚本。

### 6. 安全与性能考量
*   **安全性**: API密钥安全存储、文件系统访问可禁用、工具调用验证、超时保护和服务器进程隔离。
*   **性能**: 并发工具执行、流式响应、连接池、缓存和异步架构。

---

## English Report

### 1. Overview
The MCP CLI (Model Context Protocol Command Line Interface) is a feature-rich command-line tool designed for seamless communication with Large Language Models (LLMs) by interacting with Model Context Protocol servers. It integrates the CHUK Tool Processor and CHUK-LLM libraries, providing tool usage, conversation management, and multiple operational modes.

### 2. Core Architecture
The MCP CLI is built on a modular architecture with a clear separation of concerns, primarily composed of the following three core components:
*   **CHUK Tool Processor**: Responsible for asynchronous tool execution and communication with MCP servers.
*   **CHUK-LLM**: Provides unified LLM provider configuration and client management.
*   **MCP CLI (This Project)**: Offers a rich user interface and command orchestration capabilities.

### 3. Key Features and Capabilities
*   **Multiple Operational Modes**:
    *   **Chat Mode**: Provides a conversational interface with streaming responses and automated tool usage.
    *   **Interactive Mode**: A command-driven shell interface for direct server operations.
    *   **Command Mode**: A Unix-friendly mode suitable for script automation and pipeline operations.
    *   **Direct Commands**: Allows running individual commands without entering interactive mode.
*   **Advanced Chat Interface**: Supports streaming responses, concurrent tool execution, smart interruption, performance metrics display, and rich formatting (Markdown rendering, syntax highlighting).
*   **Comprehensive Provider Support**: Supports OpenAI, Anthropic, Ollama, and custom providers, with dynamic switching during a conversation.
*   **Robust Tool System**: Features automatic discovery of server-provided tools, provider adaptation, concurrent execution, rich progress display, tool history, and streaming tool calls.
*   **Advanced Configuration Management**: Supports configuration via environment variables and configuration files (`server_config.json`, `~/.chuk_llm/providers.yaml`, `~/.chuk_llm/.env`), along with user preferences, validation, and diagnostic functionalities.
*   **Enhanced User Experience**: Cross-platform support, rich console output, command completion, a comprehensive help system, and graceful error handling.

### 4. Technology Stack and Dependencies
*   **Core Language**: Python 3.11+
*   **LLM and MCP Related Libraries**: `anthropic`, `google-genai`, `chuk-llm`, `chuk-mcp`, `chuk-tool-processor`
*   **CLI User Interface Libraries**: `prompt-toolkit`, `rich`, `typer`
*   **Core Utility Libraries**: `asyncio` (for asynchronous programming), `python-dotenv` (for environment variable management)

### 5. Project Structure
The project has a clear structure, with the main source code located in the `src/mcp_cli/` directory, organized into functional modules:
*   `src/mcp_cli/chat/`: Contains the core logic for chat mode, including context, handler, conversation, UI, and tool processing.
*   `src/mcp_cli/cli/`: Handles the registration of main CLI commands and base commands.
*   `src/mcp_cli/commands/`: Implements general commands.
*   `src/mcp_cli/interactive/`: Contains the logic for the interactive shell mode.
*   `src/mcp_cli/llm/`: Includes the LLM client, system prompt generation, and tool handler.
*   `src/mcp_cli/tools/`: Manages tool adapters, formatting, managers, and model definitions.
*   `src/mcp_cli/ui/`: Provides UI helper functions and color definitions.
*   `src/mcp_cli/utils/`: Contains asynchronous utilities, LLM probing, and Rich library helpers.
*   `src/mcp_cli/main.py`: The main entry point for `mcp-cli`.
*   `tests/`: Contains unit and integration tests, mirroring the source code structure.
*   `diagnostics/`: Scripts for diagnostic purposes.
*   `examples/`: Scripts demonstrating usage examples.
*   `scripts/`: Contains the `mcp-cli` executable script.

### 6. Security and Performance Considerations
*   **Security**: API keys are stored securely, filesystem access can be disabled, tool calls are validated, timeouts prevent hanging operations, and server processes are isolated.
*   **Performance**: Achieved through concurrent tool execution, streaming responses, connection pooling, caching, and an asynchronous architecture.