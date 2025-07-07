# 一、ollama基础知识

## 1、什么是ollama

---

**Ollama** 是一个开源框架，专注于在本地设备上便捷地部署和运行 大型语言模型（LLM）。它为开发者和非专业用户提供了简单高效的方式来使用先进的语言模型。

### 主要特点与功能概述：

#### 1. **简化部署流程**
Ollama 的核心目标是降低大型语言模型的部署门槛，尤其针对 Docker 容器环境进行了优化。即使是非技术背景的用户，也能轻松地安装、配置并运行复杂的 LLM。

#### 2. **轻量级设计与良好扩展性**
作为一个轻量级框架，Ollama 在保持低资源占用的同时，具备良好的可扩展性。用户可根据项目需求和硬件条件灵活调整配置，适用于从个人项目到企业级应用的多种场景。

#### 3. **简洁易用的 API 接口**
Ollama 提供了直观的 API 接口，方便开发者快速创建、运行和管理模型实例。这种设计显著降低了与模型交互的技术难度，提升了开发效率。

#### 4. **丰富的预训练模型库**
框架内置了多个经过训练的大型语言模型，用户可直接调用这些模型进行推理或集成到自己的应用程序中，无需从零开始训练或自行寻找模型来源。

#### 5. **支持模型导入与定制化**

- **支持 GGUF 格式模型导入**：允许用户将来自 GGUF 平台的模型快速加载至 Ollama 环境中。
- **兼容 PyTorch 与 Safetensors 模型**：支持从主流深度学习框架（如 PyTorch 和 Safetensors）导入模型，便于已有项目的迁移与整合。
- **自定义提示工程**：提供灵活的 prompt 编辑功能，用户可以根据具体需求对模型输入提示进行修改和优化，从而引导生成特定风格或类型的输出。

#### 6. **跨平台支持**
Ollama 提供了全面的操作系统适配方案，支持 macOS、Linux、Windows（预览版）以及 Docker 环境下的部署，确保用户能够在各种平台上顺利使用。

---

## 2、ollama命令

- 使用ollama -h查看

```shell
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
```

---

### ✅ 1. `serve`：启动 Ollama 服务

```bash
ollama serve
```

> 启动本地 Ollama 服务，用于运行和管理模型。通常在后台运行，供其他命令或 API 调用。

---

### ✅ 2. `create`：创建一个模型（基于 Modelfile）

```bash
ollama create my-model -f ./Modelfile
```

> 根据当前目录下的 `Modelfile` 创建名为 `my-model` 的模型。

**Modelfile 示例内容：**

```Dockerfile
FROM llama3
PARAMETER temperature 0.7
TEMPLATE """{{ if .System }}{{ .System }}
{{ end }}{{ .User }}: {{ .Prompt }}"""
```

---

### ✅ 3. `show`：显示模型信息

```bash
ollama show llama3
```

> 显示模型 `llama3` 的详细信息，如参数、模板、系统提示等。

---

### ✅ 4. `run`：运行模型（进行推理）

```bash
ollama run llama3
```

> 启动交互式会话，输入文本后由模型生成回应。

你也可以直接传递输入：

```bash
ollama run llama3 "请写一首关于夏天的诗"
```

---

### ✅ 5. `stop`：停止正在运行的模型

```bash
ollama stop llama3
```

> 停止名为 `llama3` 的模型进程。

---

### ✅ 6. `pull`：从远程仓库拉取模型

```bash
ollama pull llama3
```

> 从官方仓库下载预训练模型 `llama3` 到本地。

支持指定标签（tag）：

```bash
ollama pull llama3:70b
```

---

### ✅ 7. `push`：推送模型到远程仓库

```bash
ollama push my-model
```

> 将本地模型 `my-model` 推送到远程模型注册中心（registry），便于共享或部署。

---

### ✅ 8. `list`：列出所有已安装模型

```bash
ollama list
```

> 输出如下格式：

```
NAME            SIZE            MODIFIED
llama3          4.7GB           2 weeks ago
mistral         2.1GB           3 days ago
```

---

### ✅ 9. `ps`：列出正在运行的模型

```bash
ollama ps
```

> 显示当前正在运行的模型及其状态，例如：

```
NAME            STATUS
llama3          running
```

---

### ✅ 10. `cp`：复制模型（重命名/备份）

```bash
ollama cp llama3 my-llama
```

> 将模型 `llama3` 复制为 `my-llama`。

---

### ✅ 11. `rm`：删除模型

```bash
ollama rm llama3
```

> 删除本地模型 `llama3`。

---

### ✅ 12. `help`：查看帮助信息

```bash
ollama help
```

> 查看所有命令的帮助信息。

指定命令帮助：

```bash
ollama run --help
```

---

### 📌 总结表格（带示例）

| 命令       | 示例命令                             | 功能描述 |
|------------|--------------------------------------|----------|
| `serve`    | `ollama serve`                       | 启动服务 |
| `create`   | `ollama create my-model -f Modelfile`| 创建模型 |
| `show`     | `ollama show llama3`                 | 显示模型详情 |
| `run`      | `ollama run llama3`                  | 运行模型 |
| `stop`     | `ollama stop llama3`                 | 停止模型 |
| `pull`     | `ollama pull llama3`                 | 拉取模型 |
| `push`     | `ollama push my-model`               | 推送模型 |
| `list`     | `ollama list`                        | 列出所有模型 |
| `ps`       | `ollama ps`                          | 列出运行中的模型 |
| `cp`       | `ollama cp llama3 my-llama`          | 复制模型 |
| `rm`       | `ollama rm llama3`                   | 删除模型 |
| `help`     | `ollama help` 或 `ollama run --help` | 查看帮助 |

---

如果你需要进一步了解某个命令的功能或参数，可以使用 `--help` 获取详细说明。例如：

```bash
ollama create --help
```
### 修改模型名

```shell
# 查看列表
ollama list
# 生成原模型的Modelfile文件
ollama show --modelfile xxxxxx > Modelfile
# 从Modelfile文件创建新的模型
ollama create DeepSeek-R1-Qwen:32B -f Modelfile 
# 删除原模型
ollama rm xxxxxx
```

# 二、ollama使用教程

## 1、安装

#### ①下载

访问：https://ollama.com/，点击 Download

![1751849751796](.\resource\1751850111562.jpg)

点击 Download for windows

![1751850060664](.\resource\1751850060664.png)

下载完成后，是一个OllamaSetup.exe文件

![1751850574508](.\resource\1751850680645.jpg)

#### ②安装

双击OllamaSetup.exe安装，点击Install，会默认安装在C盘下

![1751850762478](.\resource\1751850762478.jpg)

安装完成后，在命令窗口输入ollama -v，显示出版本号则安装成功。

![1751851111089](.\resource\1751851111089.jpg)

#### ③常用命令

见上述介绍

#### ④命令窗口对话

输入如下命令

```shell
ollama run qwen3:8b
```

![1751855210295](E:\desktop\AI课程制作\课程制作\3、ollama教程\resource\1751855210295.jpg)

#### ⑤代码调用

```python
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
payload = {
    "model": "qwen3:8b",
    "messages":  [{"role": "user", "content": "怎么做西红柿炒蛋"}],
    "stream": False  # 流式响应
}

response = requests.post(OLLAMA_API_URL, json=payload, stream=False)
# 检查HTTP状态码
response.raise_for_status()
print(response)

response_json = response.json()
# 提取消息内容
content = response_json['message']['content']
print(response_json)
print(content)
```

运行结果

![1751856255393](.\resource\1751856255393.jpg)

