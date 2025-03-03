import asyncio
import random
from playwright.async_api import BrowserContext, DOMElementNode


async def click_human(element_node: DOMElementNode, browser: BrowserContext):
    page = await browser.get_current_page()
    element = await browser.get_locate_element(element_node)

    if element is None:
        raise Exception("Element not found")

    # Получаем размеры и позицию элемента
    box = await element.bounding_box()
    if not box:
        raise Exception("Could not get element dimensions")

    # Добавляем случайное смещение внутри элемента
    # Оставляем отступ от края 5px для надежности
    offset_x = random.uniform(5, box["width"] - 5)
    offset_y = random.uniform(5, box["height"] - 5)

    # Добавляем микро-движения перед кликом
    micro_moves = random.randint(2, 4)
    for _ in range(micro_moves):
        micro_x = random.uniform(-3, 3)
        micro_y = random.uniform(-3, 3)
        await page.mouse.move(
            box["x"] + offset_x + micro_x,
            box["y"] + offset_y + micro_y
        )
        await asyncio.sleep(random.uniform(0.05, 0.1))

    # Финальное движение и клик
    await page.mouse.move(
        box["x"] + offset_x,
        box["y"] + offset_y,
        steps=random.randint(2, 4)
    )

    # Небольшая пауза перед кликом
    await asyncio.sleep(random.uniform(0.1, 0.3))

    await page.mouse.down()
    await asyncio.sleep(random.uniform(0.05, 0.15))
    await page.mouse.up()

    return f"Clicked element at offset ({offset_x:.1f}, {offset_y:.1f})"