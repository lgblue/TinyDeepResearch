from tavily import TavilyClient
def search(query: str) -> str:
    '''
    使用Tavily API搜索指定查询内容，并返回搜索结果的摘要。
    参数：
    - query: 用户输入的搜索查询字符串
    返回：
    - 搜索结果的摘要字符串
    '''
    client = TavilyClient("your_tavily_api_key")
    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5,
    )
    return response['results']