# DeepResearch

一个极简的 Deep Research Demo：
1. 先把研究主题拆成 3-5 个子任务
2. 对每个子任务执行搜索并总结
3. 汇总生成最终 Markdown 报告

## 项目结构

- `agent.py`：三个 Agent（规划、总结、报告）以及子任务解析
- `search.py`：Tavily 搜索工具封装
- `demo.py`：端到端运行入口
- `output.md`：运行后生成的报告文件（在项目根目录）

## 依赖安装

```bash
pip install langchain-openai langgraph tavily-python
```

## 配置 API Key（建议）

当前代码中在以下位置写死了 key（不推荐）：
- `backbone.py` 中 `OPENAI_API_KEY`
- `search.py` 中 `TavilyClient(...)`

建议改成环境变量：

```bash
export OPENAI_API_KEY="你的模型服务key"
export TAVILY_API_KEY="你的tavily key"
```

并在代码中读取：

- `backbone.py`：删除写死 `os.environ["OPENAI_API_KEY"] = ...`
- `search.py`：改为 `TavilyClient(os.getenv("TAVILY_API_KEY"))`

## 运行

在 `DeepResearch` 目录下执行：

```bash
python demo.py
```

运行完成后会在当前目录生成：
- `output.md`

## 流程说明

`demo.py` 的执行流程：
1. 输入研究主题
2. `PlanAgent.generate_plan()` 生成子任务 JSON
3. `extract_subtasks()` 解析子任务
4. `SummarizeAgent.summarize_task()` 对每个子任务调用搜索工具并总结
5. `ReportAgent.write_report()` 生成最终报告

## 备注

- 默认模型配置在 `backbone.py`：`Qwen/Qwen3-8B`（SiliconFlow OpenAI 兼容接口）
- 如果接口或模型名不可用，请按你的服务商配置修改 `model` 和 `base_url`

