import uvicorn
from app.core import app  # Import the FastAPI app instance

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9600, reload=True)
