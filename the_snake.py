"""Основной и единственный модуль игры 'Змейка'.

В данном модуле представлены классы GameObject, Snake, Apple.
GameObject - родительский класс для всех объектов игры.
Snake - класс, отвечающий за объект змеи и его поведения.
Apple - класс, отвечающий за объект яблока и его поведения.
Также присутствует функция handle_keys -
Она отвечает за управление объектом змея.
"""
from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь для изменения направления:
NEXT_DIRECTIONS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Множество допустимых координат:
ALL_CELLS = set(
    ((x * GRID_SIZE) % SCREEN_WIDTH, (y * GRID_SIZE) % SCREEN_HEIGHT)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

# Цвета полей и объектов:
BOARD_BACKGROUND_COLOR = (211, 211, 211)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Базовый класс для всех объектов игры."""

    def __init__(self, body_color=(0, 0, 0)) -> None:
        """Инициализация игрового объекта."""
        self.position = ((SCREEN_WIDTH // 2), SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки объектов."""

    def draw_cell(self, position, body_color=None):
        """Метод отрисовки одной ячейки игрового объекта."""
        body_color = body_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if body_color == self.body_color:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, который описывает поведение объекта яблоко."""

    def __init__(self,
                 occupied_positions=(0, 0),
                 body_color=APPLE_COLOR):
        """Инициализация игрового объекта яблоко."""
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установка случайной координаты позиции объекта."""
        self.position = choice(tuple(ALL_CELLS - set(occupied_positions)))

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, который описывает поведение объекта змеи."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """Инициализация игрового объекта змеи."""
        super().__init__(body_color)
        self.reset()

    def get_head_position(self):
        """Метод получения 'головы' объекта змеи."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        self.direction = next_direction

    def move(self):
        """Метод движения объекта змеи."""
        x, y = self.get_head_position()
        x1, y1 = self.direction
        self.positions.insert(0, ((x + GRID_SIZE * x1) % SCREEN_WIDTH,
                                  (y + GRID_SIZE * y1) % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовки объекта змеи."""
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Метод сброса игры к началу (при проигрыше)."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.last = None
        self.speed = SPEED


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            if event.key == pg.K_z and snake.speed < 31:
                snake.speed += 1
            elif event.key == pg.K_x and snake.speed > 1:
                snake.speed -= 1
            else:
                snake.update_direction(NEXT_DIRECTIONS.get(
                    (snake.direction, event.key), snake.direction))


def main():
    """Главная функция игры."""
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)
    max_score = 1

    while True:
        clock.tick(snake.speed)
        pg.display.set_caption(f'"Snake" '
                               f'Speed: {snake.speed}, '
                               f'Score: {max_score}, '
                               f'Faster: Z, '
                               f'Lower: X, '
                               f'Quit: ESC')
        handle_keys(snake)

        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            if snake.length > max_score:
                max_score += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
