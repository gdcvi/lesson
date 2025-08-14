"""
 * @author: zkyuan
 * @date: 2025/8/13 15:30
 * @description: fastapi的接口文档
"""
from fastapi import FastAPI

# 实例化
app = FastAPI(
    title="一个简单的接口文档",
    version="1.0.0",
    # 外部CDN资源
    # swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
    # swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    # swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    # swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
)


@app.post("/post",
          tags=["这是post接口标题"],
          summary="接口测试语法",
          description="这是接口的详情信息",
          response_description="响应详细信息",
          deprecated=False,  # 是否废弃
          )
async def post():
    return "post"


@app.get("/get")
async def get():
    return "get"


@app.put("/put")
async def put():
    return "put"


@app.delete("/delete")
async def delete():
    return "delete"


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
