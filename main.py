from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
