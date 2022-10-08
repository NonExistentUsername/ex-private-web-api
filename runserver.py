import os
import uvicorn

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    os.environ["BIND_PORT"] = str(port)
    uvicorn.run("app.main:app", app_dir="app", port=port, host="0.0.0.0", reload=True, workers=1)
    uvicorn.run("app.main:app", app_dir="app", port=5000, host="0.0.0.0", reload=True, workers=1)