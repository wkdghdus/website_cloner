from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import get_clone  # Uses your LangGraph workflow

app = FastAPI()

# Enable CORS (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class CloneRequest(BaseModel):
    url: str

# Response schema (optional, but useful for clarity)
class CloneResponse(BaseModel):
    generated_html: str

# Main endpoint: POST /clone
@app.post("/clone", response_model=CloneResponse)
def clone_site(request: CloneRequest):
    
    try:
        html = get_clone(request.url.strip())

        if not isinstance(html, str) or not html.strip():
            raise ValueError("HTML is empty or not a valid string.")

        return {"generated_html": html}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Health check
@app.get("/hello")
def hello():
    return {"message": "FastAPI is up and running."}

@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)