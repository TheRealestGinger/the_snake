"""Основной и единственный модуль игры 'Змейка'.

В данном модуле представлены классы GameObject, Snake, Apple.
GameObject - родительский класс для всех объектов игры.
Snake - класс, отвечающий за объект змеи и его поведения.
Apple - класс, отвечающий за объект яблока и его поведения.
Также присутствует функция handle_keys -
Она отвечает за управление объектом змея.
"""
from random import choice, randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Базовый класс для всех объектов игры."""

    def __init__(self) -> None:
        """Инициализация игрового объекта."""
        self.position = ((SCREEN_WIDTH // 2), SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Абстрактный метод отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Класс, который описывает поведение объекта яблоко."""

    def __init__(self,
                 snake_positions=(0, 0)):
        """Инициализация игрового объекта яблоко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Установка случайной координаты позиции объекта."""
        new_coordinate = ((randint(0, GRID_WIDTH) *
                           GRID_SIZE) % SCREEN_WIDTH,
                          (randint(0, GRID_HEIGHT) *
                           GRID_SIZE) % SCREEN_HEIGHT)
        while True:
            if new_coordinate not in snake_positions:
                return new_coordinate
            else:
                new_coordinate = (randint(0, GRID_HEIGHT) * GRID_SIZE,
                                  randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, который описывает поведение объекта змеи."""

    def __init__(self) -> None:
        """Инициализация игрового объекта змеи."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод получения 'головы' объекта змеи."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения объекта змеи."""
        head = self.get_head_position()
        next_position = ((head[0] +
                          GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
                         (head[1] +
                          GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT)
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Метод отрисовки объекта змеи."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса игры к началу (при проигрыше)."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        pygame.display.update()

        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[1:-1]:
            snake.reset()


if __name__ == '__main__':
    main()
