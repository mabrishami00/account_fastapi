from fastapi import FastAPI
from api.api_v1.api import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def test():
    return "test"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8002, reload=True)

