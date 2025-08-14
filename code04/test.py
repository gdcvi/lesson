"""
 * @author: zkyuan
 * @date: 2025/8/14 9:48
 * @description: 测试接口
"""

"""
测试接口的方法
    1、使用接口文档：http://127.0.0.1:8080/docs
        fastapi内置了swagger接口文档，但是内置的接口文档的网页页面需要访问国外服务器的资源，国内很难访问到，解决方案有三：
        一是切换到别的CDN资源，需要自己配置CDN资源，二是配置本地的CDN资源，这个也比较麻烦，三是使用科学上网工具，简单但非法。
    2、使用postman等工具来测，需要在电脑上安装postman软件。
    3、使用python代码的requests模块来测试，下面就是使用的这种方法。
"""

import requests

# 1、post请求   json格式的参数
url1 = "http://127.0.0.1:8080/post"   # 接口请求地址url
payload = {                           # 请求参数
    "name": "string",
    "tel": 123644,
    "age": 18
}

# 发送请求
response1 = requests.post(url1, json=payload)

# 查看请求结果
if response1.status_code == 200:   # 判断请求是否成功
    data = response1.json()  # 解析 JSON 响应
    print("请求成功！")
    print(data)
else:
    print(f"请求失败，状态码：{response1.status_code}")
    print(response1.text)  # 查看原始响应

# 2、表单参数
url2 = "http://127.0.0.1:8080/login"
response2 = requests.post(
    url2,
    data={"username": "bob", "password": "secret"},
)
if response2.status_code == 200:
    data = response2.json()  # 解析 JSON 响应
    print("请求成功！")
    print(data)
else:
    print(f"请求失败，状态码：{response2.status_code}")
    print(response2.text)  # 查看原始响应


# 3、get请求 路径参数
import requests

url3 = "http://127.0.0.1:8080/get1/22"
response = requests.get(url3)

if response.status_code == 200:
    data = response.json()  # 解析 JSON 响应
    print("请求成功！")
    print(data)
else:
    print(f"请求失败，状态码：{response.status_code}")
    print(response.text)  # 查看原始响应

# 4、查询参数
import requests

url4 = "http://127.0.0.1:8080/get2"
params = {
    "id": 100,
    "name": "zzz",
    "args": "66"
}

response = requests.get(url4, params=params)

if response.status_code == 200:
    data = response.json()  # 解析 JSON 响应
    print("请求成功！")
    print(data)
else:
    print(f"请求失败，状态码：{response.status_code}")
    print(response.text)  # 查看原始响应