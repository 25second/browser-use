
from browser_use import Agent
from langchain_openai import ChatOpenAI
from human_like_actions import controller

async def main():
    agent = Agent(
        task="Navigate to a website and interact with it naturally",
        llm=ChatOpenAI(model="gpt-4"),
        controller=controller
    )
    await agent.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
