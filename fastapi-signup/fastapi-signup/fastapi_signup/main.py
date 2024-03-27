import uvicorn
from fastapi import FastAPI
from routes.user import user_routes

app = FastAPI()

app.include_router(user_routes)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(8000)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)
