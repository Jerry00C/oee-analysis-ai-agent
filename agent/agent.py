from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import daily_shift_metric_tool, oee_trend_tool, top_scrap_day_tool


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


agent = create_agent(
    model=llm, 
    tools=[daily_shift_metric_tool, oee_trend_tool, top_scrap_day_tool],
    system_prompt=(
        "You are a car part manufacturing business analysis expert."
        "Set today is 2021-03-18"
        "Use tols whenever the user asks about actual OEE data, scrap, dates, trends, workcenters"
        "Do not invent numbers"
        "After receiving tool results, summarize clearly and briefly"
        "If not data is found, please say so explicitly response that No data is available"
    )
)