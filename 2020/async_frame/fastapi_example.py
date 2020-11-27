__doc__ = '示例'
__my__ = """
1.py3的类型注释和go的写法很相似,都是类型放在变量后面,值再放在类型后面
2.fastapi的关于request的body的解析方式也非常类似gin中的方式,先定义结构体,以及类型,用来接受body
3.
"""

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header, Form, UploadFile, BackgroundTasks

app = FastAPI(title="My Example Project",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="0.0.1", )


@app.get("/")
def read_root():
    # time.sleep(2)
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("fastapi_example:app", host="127.0.0.1", port=8000, log_level="info")
