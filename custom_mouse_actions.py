
from browser_use import Controller
from pydantic import BaseModel

# Создаем модели для параметров
class MouseMoveAction(BaseModel):
    x: int
    y: int
    steps: int = 1

class MouseDragAction(BaseModel):
    start_x: int 
    start_y: int
    end_x: int
    end_y: int
    steps: int = 1

# Создаем контроллер
controller = Controller()

@controller.action("Move mouse to specific coordinates with optional steps for smooth movement")
async def move_mouse(params: MouseMoveAction, browser):
    page = await browser.get_current_page()
    await page.mouse.move(params.x, params.y, steps=params.steps)
    return f"Moved mouse to coordinates ({params.x}, {params.y})"

@controller.action("Click at current mouse position") 
async def click_at_position(browser):
    page = await browser.get_current_page()
    await page.mouse.click(0, 0) # Кликает в текущей позиции
    return "Clicked at current position"

@controller.action("Drag mouse from start to end coordinates")
async def drag_mouse(params: MouseDragAction, browser):
    page = await browser.get_current_page()
    await page.mouse.move(params.start_x, params.start_y, steps=1)
    await page.mouse.down()
    await page.mouse.move(params.end_x, params.end_y, steps=params.steps)
    await page.mouse.up()
    return f"Dragged from ({params.start_x}, {params.start_y}) to ({params.end_x}, {params.end_y})"
