from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return "This is an index page"
