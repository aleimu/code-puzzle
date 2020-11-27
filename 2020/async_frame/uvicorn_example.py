# coding:utf-8
__doc__ = """
最简单的ASGI服务示例
从fastapi直接去读源码,会在uvicorn中的 uvloop和httptools与 asyncio的交互中迷路,
所以暂时先从最简单的app来了解uvicorn是如何运作的,如何在事件循环中接受请求,处理请求,发送返回等
然后再看starlette是如何封装uvicorn,以及fastapi又是如何封装starlette的.
"""

import uvicorn


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ]
    })
    print("tag!!!")
    await send({
        'type': 'http.response.body',
        'body': b'uvicorn say: Hello, world!',
    })


if __name__ == "__main__":
    uvicorn.run("uvicorn_example:app", host="127.0.0.1", port=9000, log_level="info")
