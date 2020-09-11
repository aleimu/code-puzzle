__doc__ = '示例'
__my__ = """
1.py3的类型注释和go的写法很相似,都是类型放在变量后面,值再放在类型后面
2.fastapi的关于request的body的解析方式也非常类似gin中的方式,先定义结构体,以及类型,用来接受body
3.
"""

import time
from typing import List, Set, Tuple, Dict, Any
from fastapi import FastAPI, Query, Path, Body, Header, Form, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse,Response
from fastapi import *
from pydantic import BaseModel, Field, HttpUrl, EmailStr
import asyncio

from types import FunctionType

# 通用类型
def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes], test: List[str], prices: Dict[str, float]):
    for item in test:
        print(item)
    for item_name, item_price in prices:
        print(item_name)
        print(item_price)
    return items_t, items_s


class Person:
    def __init__(self, name: str):
        self.name = name


# 自定义类型
def get_person_name(one_person: Person):
    return one_person.name


app = FastAPI(title="My Super Project",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="2.5.0", )


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)  # 错误处理
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.middleware("http")  # 中间件
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_root():
    # time.sleep(2)
    return {"Hello": "World"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    if not username:
        raise HTTPException(
            status_code=404,
            detail="username not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"username": username}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# Path Parameters
# curl "http://127.0.0.1:8000/test/123"
# curl "http://127.0.0.1:8000/test/123?q=123"
@app.get("/test/{uid}")
def read_item(uid: int, q: str = None):
    return {"uid": uid, "q": q}


# Query Parameters
# curl "http://127.0.0.1:8000/test/?skip=1&limit=1"
@app.get("/test/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


class Item(BaseModel):  # TODO 类似于gin中的先定义结构体用来承载body
    name: str
    price: float
    is_offer: bool = None


# Request Body
# curl -X PUT "http://127.0.0.1:8000/test/1" -d "name=12&price=123&is_offer=123"   // 错误
# curl -X PUT "http://127.0.0.1:8000/test/1" -d "{\"name\":12,\"price\":123,\"is_offer\":false}" //正确
@app.put("/test/{uid}")
def update_item(uid: int, item: Item):
    return {"item_name": item.name, "uid": uid}


# 设定q的类型,默认值,以及最大长度,甚至是正则匹配
# curl "http://127.0.0.1:8000/test1/?q=fixedquery"
@app.get("/test1/{uid}")
async def read_items(
        uid: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
        q: str = Query('fixedquery', min_length=3, max_length=50, regex="^fixedquery$", title="Query string"),
        size: float = Query(..., gt=0, lt=10.5)):
    results = {"test": [{"uid": "Foo"}, {"uid": "Bar"}], 'uid': uid}
    if q:
        results.update({"q": q})
    return results


@app.get("/test4/", status_code=201)
async def read_items(*, user_agent: str = Header(None)):
    return {"User-Agent": user_agent}


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: float = None
    images: List[Image] = None

    class Config:  # 声明一个例子使用配置和schema_extra，在Pydantic的文档所描述的一个Pydantic模式：定制模式
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class User(BaseModel):
    username: str
    full_name: str = None
    image: Image = None  # 套娃


@app.put("/test2/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item = Body(
            ...,
            example={
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
        ),
        user: User,
        importance: int = Body(..., gt=0),
        q: str = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.route("/test2/{id}", methods=['PUT', "GET", 'POST'])
def test1(id: str):
    time.sleep(2)
    return {"test1": id}


@app.get("/test3/{id}")
def test2(id: str):
    time.sleep(2)
    return {"test2": id}


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


if __name__ == "__main__":
    # uvicorn scratch_49:app --reload 命令行启动或下面的脚本式启动
    import uvicorn

    uvicorn.run("fastapi_demo:app", host="127.0.0.1", port=8000, log_level="info")
