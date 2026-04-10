# complex-workflow-automation-and-evaluation
Automate a multi-step task with API exposure and frontend interaction
# 🤖 AI Research Assistant – Multi-Agent Workflow (Milestone 4)

## 📌 Project Overview

This project implements a **multi-agent AI system** using a workflow-based architecture.
It allows users to input a query and automatically processes it through multiple AI agents to generate structured outputs.

---

## 🎯 Objective

To design and implement a **complex multi-step workflow** using:

* Multiple AI agents
* REST API (FastAPI)
* Frontend user interface
* Automated task orchestration

---

## 🧠 System Architecture

```text
User (Frontend UI)
        ↓
     FastAPI API
        ↓
 Orchestrator Function
        ↓
🔍 Research Agent
        ↓
📝 Summarizer Agent
        ↓
✉️ Email Agent
        ↓
 Final Output (UI)
```

---

## 🤖 Agents Description

### 🔍 Research Agent

* Generates detailed answers for user queries
* Uses TinyLlama-1.1B-Chat model

### 📝 Summarizer Agent

* Converts detailed content into short summaries
* Improves readability and clarity

### ✉️ Email Agent

* Converts summarized content into a professional email format
* Useful for real-world communication

---

## 🔄 Workflow

1. User enters a query in the frontend
2. API receives the request
3. Research Agent generates detailed content
4. Summarizer Agent shortens the content
5. Email Agent formats the output
6. Final response is sent back to UI

---

## ⚙️ Technologies Used

* Python
* FastAPI
* HuggingFace Transformers
* TinyLlama-1.1B-Chat Model
* HTML, CSS, JavaScript (Frontend)

---

## 📡 API Endpoints

### 🔹 Health Check

```
GET /health
```

### 🔹 Run Workflow

```
POST /workflow
```

#### Request:

```json
{
  "query": "What is Artificial Intelligence?"
}
```

#### Response:

```json
{
  "research": "...",
  "summary": "...",
  "email": "..."
}
```

---

## 🖥️ Frontend

* Interactive chat interface
* Displays AI responses in real-time
* Connected to FastAPI backend

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```bash
pip install fastapi uvicorn transformers torch
```

### 2️⃣ Run the Server

```bash
python milestone4.py
```

### 3️⃣ Open in Browser

```
http://localhost:8000/
```

---

## 🧪 Example

### Input:

```
Explain Artificial Intelligence
```

### Output:

* Research: Detailed explanation
* Summary: Short version
* Email: Professional formatted message

---

## 🏆 Key Features

* Multi-agent orchestration
* Automated workflow execution
* REST API integration
* Interactive web interface
* Real-world task automation

---

## 📊 Evaluation

The system successfully:

* Executes multi-step workflows
* Uses multiple agents collaboratively
* Provides structured outputs
* Supports frontend interaction

---

## 📌 Conclusion

This project demonstrates how AI agents can collaborate in a structured workflow to automate complex tasks. It integrates backend processing, API communication, and frontend interaction into a single system.

---

## 🚀 Future Improvements

* Add memory for context-aware responses
* Improve model accuracy using FLAN-T5 or LLaMA
* Deploy the system online
* Add user authentication

---
