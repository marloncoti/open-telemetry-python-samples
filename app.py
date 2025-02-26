from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}

@app.get("/add")
async def add_numbers(a: int, b: int):
    result = a + b
    return {"operation": f"{a} + {b}", "result": result}
    

@app.get("/search_name")
async def call_external_api(name: str = 'Kevin'):
    response = requests.get(f"https://api.snationalize.io?name={name}")  
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data from external API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
