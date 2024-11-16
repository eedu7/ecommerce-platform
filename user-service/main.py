import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="core.server:app",
        reload=True,
        port=8002,
    )
