"""
 * @author: zkyuan
 * @date: 2025/8/13 15:20
 * @description: fastapi第一个接口
"""

# 安装依赖
# pip install fastapi
# pip install uvicorn
from fastapi import FastAPI

# 实例化
app = FastAPI()


@app.post("/update")
async def update():
    return "messages:200, ok!"


@app.get("/get")
async def get():
    return "success，这里是get请求"


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

# 在postman调用接口访问
# 接口文档  http://localhost:8080/docs
# 命令运行：uvicorn 文件名:app --reload --port=8080 --host=127.0.0.1