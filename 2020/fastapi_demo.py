from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import time
from asyncio import sleep
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="./dome"), name="static")


@app.get("/")
async def read_root():
    # time.sleep(5)
    # await sleep(5)
    return FileResponse('./scratch_17.py', filename='test.txt')
    # return StreamingResponse('./scratch_17.py', filename='test.txt')
    # return {"Hello": "World"}


@app.get("/img/")
async def getImgApi():
    buffer = io.BytesIO(b'./scratch_17.py')
    return StreamingResponse(buffer)  # 创建响应体


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
