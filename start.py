from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
 
async def main():
    agent = Agent(
        task="go to https://docs.browser-use.com/introduction documentatiomn and search if there is option for screening to frontend",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
