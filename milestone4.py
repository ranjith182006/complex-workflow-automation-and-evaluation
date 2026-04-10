import os
import socket
import re
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI(title="AI Research Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str

# Static files
base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Load Tiny Llama 1.1B Chat Model
print("Loading Tiny Llama 1.1B Chat model...")
model_name = "TinyLlama/TinyLlama-1.1b-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="auto"
)
print("Model loaded successfully!")

# Answer generator using Tiny Llama 1.1B Chat
def generate_answer(query: str) -> str:
    """Generate an answer using Tiny Llama 1.1B Chat model"""
    try:
        # Format input as chat
        prompt = f"<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n"
        
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=512,
                min_length=10,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the answer part (after assistant response)
        if "<|im_start|>assistant" in response:
            answer = response.split("<|im_start|>assistant")[-1].strip()
        else:
            answer = response.split(prompt)[-1].strip() if prompt in response else response
            
        return answer if answer else "I couldn't generate a response. Please try again."
        
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AI Research Assistant"}

@app.post("/workflow", response_model=QueryResponse)
async def answer_query(request: QueryRequest):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    answer = generate_answer(request.query)
    return QueryResponse(query=request.query, answer=answer)

# Server
if __name__ == "__main__":
    import uvicorn
    import time
    
    base_port = int(os.environ.get("PORT", 8000))
    started = False
    
    for attempt in range(10):
        port = base_port + attempt
        try:
            print(f"\nStarting AI Assistant on http://localhost:{port}")
            print(f"Static: http://localhost:{port}/static/")
            print(f"API: http://localhost:{port}/workflow\n")
            
            uvicorn.run(
                app, 
                host="0.0.0.0", 
                port=port, 
                log_level="info"
            )
            started = True
            break
        except OSError as e:
            error_msg = str(e).lower()
            if "address already in use" in error_msg or "errno 10048" in error_msg:
                print(f"Port {port} busy, trying {port + 1}...")
                time.sleep(0.5)
                continue
            else:
                print(f"Fatal error: {e}")
                raise
        except Exception as e:
            print(f"Error on port {port}: {e}")
            time.sleep(0.5)
            continue
    
    if not started:
        print("Could not start server on any port!")
