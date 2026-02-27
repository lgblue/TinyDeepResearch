from backbone import LLMClient
import json
import re

def extract_subtasks(plan_output: str) -> list[dict]:
    """
    从plan输出中提取subtasks并转换为list[dict]格式
    
    Args:
        plan_output: PlanAgent.generate_plan()的返回文本
        
    Returns:
        list[dict]: 包含title、intent、query的字典列表
    """
    # 方法1: 使用正则表达式提取<subtasks>标签内的内容
    match = re.search(r"<subtasks>(.*?)</subtasks>", plan_output, re.DOTALL)
    if not match:
        raise ValueError("未找到<subtasks>标签")
    json_str = match.group(1)
    return json.loads(json_str)


todo_planner_instructions = """
你是一个研究规划专家。你的任务是将用户的研究主题分解为3-5个子任务。

当前日期：{current_date}

研究主题：{research_topic}

请分析这个研究主题，将其分解为3-5个子任务。每个子任务应该：
1. 涵盖主题的一个重要方面
2. 有明确的研究目标
3. 可以通过搜索引擎找到相关资料

请以JSON格式返回子任务列表，并使用<subtasks>和</subtasks>标签包裹整个列表，每个子任务包含：
- title：任务标题（简洁明了）
- intent：任务意图（为什么要研究这个）
- query：搜索查询（用于搜索引擎的查询字符串，可以使用英文以获得更好的搜索结果）

示例输出：
<subtasks>
[
  {{
    "title": "什么是多模态模型",
    "intent": "了解多模态模型的基础概念，为后续研究打下基础",
    "query": "multimodal model definition concept 2024"
  }},
  ...
]
</subtasks>

请确保：
1. 子任务数量在3-5个之间
2. 子任务之间有逻辑关系（如从基础到应用，从现状到趋势）
3. 搜索查询能够准确找到相关资料
4. 只返回JSON，不要包含其他文本
"""

task_summarizer_instructions = """
你是一个任务总结专家。你的任务是对任务进行搜索并总结搜索结果，提取关键信息。

任务标题：{task_title}
任务意图：{task_intent}
搜索查询：{task_query}

请使用搜索查询在搜索引擎中查找相关资料，并仔细阅读搜索结果。然后提取关键信息，并以Markdown格式返回总结。

总结应该包含：
1. **核心观点**：搜索结果中的核心观点和结论
2. **关键数据**：重要的数字、日期、名称等
3. **来源引用**：为每个观点添加来源引用（使用[1]、[2]等标记）

请确保：
1. 总结简洁明了，避免冗余
2. 保留重要的细节和数据
3. 为每个观点添加来源引用
4. 使用Markdown格式（标题、列表、加粗等）

示例输出：
## 核心观点

多模态模型是一种能够处理多种类型数据的AI模型[1]。与传统的单模态模型不同，多模态模型可以同时理解文本、图像、音频等[2]。

**关键特点：**
- 跨模态理解[1]
- 统一表示[3]
- 端到端训练[2]

## 来源

[1] https://example.com/source1
[2] https://example.com/source2
[3] https://example.com/source3
"""

report_writer_instructions = """
你是一个报告撰写专家。你的任务是整合所有子任务的总结，生成一份结构化的研究报告。

研究主题：{research_topic}

子任务总结：
{task_summaries}

请整合以上所有子任务的总结，生成一份结构化的研究报告。

报告应该包含：
1. **标题**：研究主题
2. **概述**：简要介绍研究主题和报告结构（2-3段）
3. **各个子任务的详细分析**：按照逻辑顺序组织（使用二级标题）
4. **总结**：总结研究的主要发现（1-2段）
5. **参考文献**：所有来源引用（按照子任务分组）

请确保：
1. 报告结构清晰，逻辑连贯
2. 消除重复的信息
3. 保留所有来源引用
4. 使用Markdown格式

示例输出：
# 多模态大模型的最新进展

## 概述

本报告系统地研究了多模态大模型的最新进展...

## 1. 什么是多模态模型

（此处插入子任务1的总结）

## 2. 最新的多模态模型有哪些

（此处插入子任务2的总结）

...

## 总结

通过本次研究，我们了解了...

## 参考文献

### 任务1：什么是多模态模型
[1] https://example.com/source1
...
"""

class PlanAgent:
    def __init__(self):
        self.llm_client = LLMClient()

    def generate_plan(self, query):
        return self.llm_client.generate_response(todo_planner_instructions.format(current_date="2026-01-01", research_topic=query), [])
  
class SummarizeAgent:
    def __init__(self):
        self.llm_client = LLMClient()

    def summarize_task(self, task_title, task_intent, task_query, tools):
        return self.llm_client.generate_response(task_summarizer_instructions.format(task_title=task_title, task_intent=task_intent, task_query=task_query), tools)
  
class ReportAgent:
    def __init__(self):
        self.llm_client = LLMClient()

    def write_report(self, research_topic, task_summaries):
        return self.llm_client.generate_response(report_writer_instructions.format(research_topic=research_topic, task_summaries=task_summaries), [])
