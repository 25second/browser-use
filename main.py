
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

load_dotenv()

async def main():
    # Конфигурация браузера с подключением через debug port
    browser = Browser(
        config=BrowserConfig(
            connect_to_cdp="http://localhost:9222",
            new_context_config=BrowserContextConfig(
                viewport_expansion=0,  # Более реалистичный viewport
                highlight_elements=False,  # Отключаем подсветку для большей естественности
                wait_between_actions=2.0  # Добавляем паузы между действиями
            ),
        ),
    )

    # Инициализация агента
    agent = Agent(
        task="Your task here",  # Замените на вашу задачу
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
        save_conversation_path="logs/conversation",  # Сохранение диалога
        generate_gif=True,  # Создание GIF с действиями
    )

    # Запуск агента
    history = await agent.run()
    
    # Сохранение истории действий
    agent.save_history("agent_history.json")

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
