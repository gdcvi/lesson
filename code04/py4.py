"""
 * @author: zkyuan
 * @date: 2025/8/13 15:31
 * @description: 参数传递
"""

# pip install python-multipart
import os
from typing import List

from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel, Field, validator


# pydantic嵌套封装
class Data(BaseModel):
    name: str
    tel: int = 123644
    age: int = Field(default=18, gt=0, lt=100)  # 默认、最小、最大

    # 校验参数
    @validator("name")
    def paramjiaoyan(cls, value):
        assert value.isalpha(), "name 必须是 alpha"
        return value

    # 参数校验
    @validator("tel")
    def paramjiaoyan(cls, value):
        assert type(value) is int, "tel 必须是 int"
        return value


# 实例化
app = FastAPI()


@app.post("/post",
          tags=["这是post接口标题"],
          summary="接口测试语法",
          description="这是接口的详情信息",
          response_description="响应详细信息",
          deprecated=False,  # 是否废弃
          )
async def post(datajson: Data):  # 请求体 前端json格式参数--->Data类型
    print(type(datajson))
    print(datajson.name)
    print(datajson.tel)
    return "post", datajson


# 请求返回的消息码
class Messages(BaseModel):
    code: int
    msg: str
    data: dict


# 表单参数 x-www-form-urlencoded
@app.post("/login")
async def login(username: str = Form(),
                password: str = Form()):  # 表单参数
    print(f"username:{username}, password:{password}")
    return Messages(code=200, msg="success", data={"out": "success"})


# 请求头参数，路径参数（路径上{}指定参数，对应函数参数）
@app.get("/get1/{id}")
async def get1(id: int):
    return "get1", id


# 请求头参数，请求参数也叫查询参数（只需要在函数中有参数,部分参数可为空）
@app.get("/get2")
async def get2(id: int = 100, name: str = None, **args):
    return "get2", id, name


# 请求头参数，查询参数和路径参数一起
@app.get("/get3/{id}")
async def get3(id: int, name: str, **args):
    return "get3", id, name


# 文件上传,字节流 文件参数
@app.post("/upfilebytes")
async def upfilebytes(file: List[bytes] = File()):
    print(f"file:{file}")
    return Messages(code=200, msg="success", data={"out": "upfilebytes文件上传成功"})


# 单个文件上传
@app.post("/upfile")
async def upfile(file: UploadFile):  # 文件名和文件内容两部分
    print(f"file:{file},filename:{file.filename}")
    # 接收文件，file文件夹要手动创建
    path = os.path.join("file", file.filename)
    # rb wb 二进制读写 不支持encoding='utf-8'
    with open(path, "wb") as f:
        for i in file.file:
            f.write(i)
    return Messages(code=200, msg="success", data={"out": "UploadFile文件上传成功"})


# 文件操作https://geek-docs.com/fastapi/fastapi-questions/284_fastapi_send_and_receive_file_using_python_fastapi_and_requests.html

# 文件列表
@app.post("/upfilelist")
async def upfilelist(filelist: List[UploadFile]):
    print(f"filelist:{filelist}")
    for file in filelist:
        print(f"filename:{file.filename},file:{file.file}")
    return Messages(code=200, msg="success", data={"out": "upfilelist文件上传成功"})


@app.put("/put")
async def put():
    return "put"


@app.delete("/delete")
async def delete():
    return "delete"


if __name__ == '__main__':
    import uvicorn

    # uvicorn.run(app, host="127.0.0.1", port=8080)
    # 加上一下参数，app要写成 文件:app 的形式
    uvicorn.run("py4:app", host="127.0.0.1", port=8080, reload=True)
