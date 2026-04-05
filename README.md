# 🏮 Local-LLM Platform: TinyLlama Edition

[![Python 64-bit](https://img.shields.io/badge/Python-3.10%20--%203.13%20(64--bit)-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Transformers](https://img.shields.io/badge/Framework-Transformers-orange.svg)](https://huggingface.co/docs/transformers/index)
[![Model: TinyLlama](https://img.shields.io/badge/Model-TinyLlama--1.1B--Chat-brightgreen.svg)](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)

A high-performance, **production-ready local LLM platform** built on the TinyLlama (1.1B Chat) architecture. This project provides a full-stack AI experience, including a REST API server, an interactive CLI chat, and fine-tuning capabilities, all running locally on your hardware.

---

## 📖 Table of Contents
* [Features](#-features)
* [Architecture](#-architecture)
* [Prerequisites](#-prerequisites)
* [Quick Start](#-quick-start)
* [Usage](#-usage)
* [Project Structure](#-project-structure)
* [Configuration](#-configuration)
* [Troubleshooting](#-troubleshooting)

---

## 🌟 Features

- **⚡ Instant Response**: TinyLlama (1.1B) delivers near-instant token generation on modern CPUs.
- **🛡️ 100% Private**: All data stays on your local machine; No data goes to external servers.
- **💬 Conversational Memory**: CLI chat and API endpoints support context-aware conversation history.
- **📡 REST API**: FastAPI server for seamless integration with external web apps and mobile apps.
- **🚀 Efficiency**: Optimized for 64-bit systems with minimal RAM footprint (~2GB).

---

## 🏗️ Architecture

| Component | Technology | Description |
|---|---|---|
| **Engine** | PyTorch & Transformers | Core ML library for inference. |
| **Model** | TinyLlama-1.1B-Chat | Advanced, compact language model. |
| **API** | FastAPI / Uvicorn | High-performance async REST interface. |
| **Logger** | Loguru | Structured application logging. |

---

## 📋 Prerequisites

* **Operating System**: Windows 64-bit (Required for PyTorch).
* **Python**: 3.10 to 3.13 (**64-bit version ONLY**).
* **Storage**: 2GB free space.
* **Memory**: 4GB+ RAM.

---

## 🚀 Quick Start

### 1. Verification
Before starting, ensure you have **64-bit Python** installed:
```powershell
python -c "import platform; print(platform.architecture())"
# Expected output: ('64bit', 'WindowsPE')
```

### 2. Dependency Setup
Install the core requirements:
```bash
pip install torch transformers accelerate datasets loguru fastapi uvicorn pydantic python-dotenv
```

### 3. Interactive Chat
Start the interactive model session (first run will download ~2GB):
```bash
python main.py --interactive
```

---

## 💬 Usage

### 🖥️ CLI Commands
- `clear`: Reset conversation context.
- `history`: Display current session history.
- `exit`: Quit the application.

### 🌐 API Server
Launch the server to expose the model as a service:
```bash
python api_server.py
```
The API is available at `http://localhost:8000`.

---

## 📂 Project Structure

```text
├── main.py              # Main entry point (Chat/Inference)
├── api_server.py        # FastAPI server implementation
├── model_manager.py     # Model loading and tokenization logic
├── config.py            # Environment and config management
├── .env                 # Project settings and secrets
├── model_cache/         # Saved model weights
└── logs/                # Application runtime logs
```

---

## ⚙️ Configuration (.env)

| Variable | Description | Default |
|---|---|---|
| `MODEL_NAME` | Model identifier from Hugging Face | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |
| `MAX_LENGTH` | Maximum tokens for generation | `256` |
| `TEMPERATURE` | Randomness of generation | `0.7` |

---

## 🛠️ Troubleshooting

- **Error: "No module named 'torch'"**: Ensure you are using 64-bit Python. 32-bit Python does not support Torch on Windows.
- **Slowness on First Run**: The model must download weights (~2GB) and initialize. Subsequent runs will be significantly faster.
- **Out of Memory**: Close heavy applications. TinyLlama only needs ~2.5GB of free RAM to buffer models.

---

## 📜 License

This project is distributed under the **MIT License**. We specifically chose this open-source license because it offers maximum freedom and minimal restrictions for the community.

### Why MIT License?
**✅ Pros (What you can do):**
- **Maximum Freedom**: Anyone can use, copy, modify, distribute, and even sell this code. 
- **Commercial Use Ready**: You can integrate this TinyLlama platform into your paid, closed-source SaaS products or apps without owing us anything.
- **No Liability**: The code is provided "as is." If you break your servers running this, we are not legally responsible.

**❌ Cons (What to realize):**
- **No Forced Sharing**: If you make huge performance improvements to our implementation, you aren't legally forced to share those improvements back to this repository (though we'd love it if you did!).

See the [LICENSE](LICENSE) file for more information.

---
**Maintained by Akash Rathod ** |https://github.com/akash-rathod01
