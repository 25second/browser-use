
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

from random import gauss
import math

def generate_bezier_curve(start_x, start_y, end_x, end_y, control_points=2):
    points = [(start_x, start_y)]
    
    # Add random control points
    for _ in range(control_points):
        cx = start_x + (end_x - start_x) * gauss(0.5, 0.2)
        cy = start_y + (end_y - start_y) * gauss(0.5, 0.2)
        points.append((cx, cy))
    
    points.append((end_x, end_y))
    return points

def calculate_bezier_point(points, t):
    n = len(points) - 1
    x = y = 0
    for i, point in enumerate(points):
        coefficient = math.comb(n, i) * (1 - t)**(n - i) * t**i
        x += point[0] * coefficient
        y += point[1] * coefficient
    return (x, y)

@controller.action("Move mouse to specific coordinates with human-like movement")
async def move_mouse(params: MouseMoveAction, browser):
    page = await browser.get_current_page()
    
    # Get current mouse position
    current_pos = await page.evaluate('({x: window.mouseX, y: window.mouseY})')
    start_x = current_pos.get('x', 0)
    start_y = current_pos.get('y', 0)
    
    # Generate curve points
    curve_points = generate_bezier_curve(start_x, start_y, params.x, params.y)
    
    # Move along curve with variable speed
    steps = max(int(math.sqrt((params.x - start_x)**2 + (params.y - start_y)**2) / 10), 20)
    
    for i in range(steps):
        t = i / (steps - 1)
        # Add slight randomness to timing
        delay = gauss(1.5, 0.5)
        await asyncio.sleep(delay/1000)
        
        x, y = calculate_bezier_point(curve_points, t)
        await page.mouse.move(x, y)
    
    return f"Moved mouse naturally to ({params.x}, {params.y})"

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
