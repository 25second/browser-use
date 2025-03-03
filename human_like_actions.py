
import random
import asyncio
import math
from typing import Optional, Tuple, List
from dataclasses import dataclass
from browser_use import Controller
from pydantic import BaseModel

@dataclass
class Point:
    x: float
    y: float

class MouseActionParams(BaseModel):
    x: int
    y: int
    duration: float = 1.0
    steps: int = 50

class ScrollParams(BaseModel):
    distance: int
    duration: float = 1.0
    steps: int = 20

controller = Controller()

def bezier_curve(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
    """Вычисляет точку на кривой Безье"""
    x = (1-t)**3 * p0.x + 3*(1-t)**2 * t * p1.x + 3*(1-t) * t**2 * p2.x + t**3 * p3.x
    y = (1-t)**3 * p0.y + 3*(1-t)**2 * t * p1.y + 3*(1-t) * t**2 * p2.y + t**3 * p3.y
    return Point(x, y)

def generate_human_curve(start: Point, end: Point) -> Tuple[Point, Point]:
    """Генерирует контрольные точки для человекоподобной кривой"""
    dist = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)
    variance = dist * 0.4
    
    # Случайные отклонения для контрольных точек
    p1 = Point(
        start.x + (end.x - start.x) * random.uniform(0.2, 0.4) + random.uniform(-variance, variance),
        start.y + (end.y - start.y) * random.uniform(0.2, 0.4) + random.uniform(-variance, variance)
    )
    
    p2 = Point(
        start.x + (end.x - start.x) * random.uniform(0.6, 0.8) + random.uniform(-variance, variance),
        start.y + (end.y - start.y) * random.uniform(0.6, 0.8) + random.uniform(-variance, variance)
    )
    
    return p1, p2

async def simulate_human_delay():
    """Симулирует случайные задержки человеческих действий"""
    base_delay = random.gauss(0.1, 0.03)
    await asyncio.sleep(max(0.01, base_delay))

@controller.action("Move mouse with human-like movement")
async def move_mouse_human(params: MouseActionParams, browser):
    page = await browser.get_current_page()
    
    # Получаем текущую позицию мыши
    current_pos = await page.evaluate('({x: window.mouseX || 0, y: window.mouseY || 0})')
    start = Point(current_pos['x'], current_pos['y'])
    end = Point(params.x, params.y)
    
    # Генерируем контрольные точки для кривой Безье
    p1, p2 = generate_human_curve(start, end)
    
    # Перемещаем мышь по кривой
    for i in range(params.steps):
        t = i / (params.steps - 1)
        
        # Добавляем микро-колебания
        wobble = Point(
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        
        point = bezier_curve(start, p1, p2, end, t)
        await page.mouse.move(
            point.x + wobble.x,
            point.y + wobble.y
        )
        
        # Случайные задержки между движениями
        await simulate_human_delay()
    
    return f"Moved mouse to ({params.x}, {params.y})"

@controller.action("Click with human-like behavior")
async def click_human(browser):
    page = await browser.get_current_page()
    
    # Случайная задержка перед кликом
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    # Имитация микродвижений при клике
    current_pos = await page.evaluate('({x: window.mouseX || 0, y: window.mouseY || 0})')
    x, y = current_pos['x'], current_pos['y']
    
    # Небольшое дрожание перед кликом
    for _ in range(random.randint(2, 4)):
        await page.mouse.move(
            x + random.uniform(-1, 1),
            y + random.uniform(-1, 1)
        )
        await asyncio.sleep(random.uniform(0.01, 0.03))
    
    # Сам клик
    await page.mouse.down()
    await asyncio.sleep(random.uniform(0.05, 0.1))
    await page.mouse.up()
    
    return "Performed human-like click"

@controller.action("Scroll with human-like behavior")
async def scroll_human(params: ScrollParams, browser):
    page = await browser.get_current_page()
    
    chunk_size = params.distance / params.steps
    accumulated_scroll = 0
    
    for i in range(params.steps):
        # Добавляем случайные отклонения к скорости скролла
        variation = chunk_size * random.uniform(0.8, 1.2)
        
        # Замедление в начале и конце скролла
        progress = i / params.steps
        ease = math.sin(progress * math.pi)
        
        current_scroll = variation * ease
        accumulated_scroll += current_scroll
        
        await page.mouse.wheel(0, current_scroll)
        
        # Случайные паузы между скроллами
        await asyncio.sleep(params.duration / params.steps * random.uniform(0.8, 1.2))
    
    return f"Scrolled {accumulated_scroll} pixels"

@controller.action("Type text with human-like behavior")
async def type_text_human(text: str, browser):
    page = await browser.get_current_page()
    
    for char in text:
        # Базовая задержка между символами
        base_delay = random.gauss(0.1, 0.02)
        
        # Увеличиваем задержку для определенных случаев
        if char in '.,!?':  # Пауза после знаков препинания
            base_delay *= 1.5
        elif char.isupper():  # Пауза для заглавных букв
            await asyncio.sleep(0.1)
            
        # Случайные опечатки
        if random.random() < 0.02:  # 2% шанс опечатки
            wrong_char = chr(ord(char) + 1)
            await page.keyboard.type(wrong_char)
            await asyncio.sleep(0.2)
            await page.keyboard.press('Backspace')
            await asyncio.sleep(0.1)
            
        await page.keyboard.type(char)
        await asyncio.sleep(base_delay)
        
        # Случайные паузы для реалистичности
        if random.random() < 0.1:  # 10% шанс более длинной паузы
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
    return f"Typed text: {text}"
