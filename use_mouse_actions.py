
from browser_use import Agent
from langchain_openai import ChatOpenAI
from custom_mouse_actions import controller

async def main():
    agent = Agent(
        task="Move mouse around and interact with page",
        llm=ChatOpenAI(model="gpt-4"),
        controller=controller
    )
    await agent.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
