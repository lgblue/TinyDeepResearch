from agent import PlanAgent, SummarizeAgent, ReportAgent, extract_subtasks
from search import search

plan_agent = PlanAgent()
summarizer_agent = SummarizeAgent()
report_agent = ReportAgent()
query = "干什么事情可以创业赚钱？"
print(f"正在研究: {query}...")
tools = [search]
plan = plan_agent.generate_plan(query)
subtasks = extract_subtasks(plan)
summarys = []
for subtask in subtasks:
    title = subtask['title']
    intent = subtask['intent']
    query = subtask['query']
    summary = summarizer_agent.summarize_task(title, intent, query, tools)
    summarys.append((title, summary))
print(f"研究已完成,正在整理结果...")
report = report_agent.write_report(query, summarys)
with open(f"output.md", "w", encoding="utf-8") as f:
    f.write(report)
print(f"最终研究报告已生成，并保存到 output.md 文件中")




