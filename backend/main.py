
from fastapi import FastAPI
from pydantic import BaseModel
from shared.agent import get_agent
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import HTTPException

load_dotenv()

app = FastAPI()
agent = get_agent()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(query: Query):
    try:
        response = agent.invoke(query.question)
        
        # Fix: Extract just the output text from the response
        if isinstance(response, dict):
            # If response is a dictionary, get the 'output' field
            answer_text = response.get('output', str(response))
        else:
            # If response is a string or other type, convert to string
            answer_text = str(response)
        
        return {"answer": answer_text}
        
    except Exception as e:
        print(f"Error in agent: {e}")
        raise HTTPException(status_code=500, detail="Agent failed to respond.")