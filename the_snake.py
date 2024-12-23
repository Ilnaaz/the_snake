from random import randint

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
SPEED = 16.6667

# Стартовая позиция змейки
POSITION_X = GRID_WIDTH // 2 * GRID_SIZE
POSITION_Y = GRID_HEIGHT // 2 * GRID_SIZE
SNAKE_START_POSITION = (POSITION_X, POSITION_Y)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка - 1')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Абстрактный класс игрового объекта,
    является предком всех классов объектов на экране.

    Атрибуты
    --------------
    color : tuple(int, int, int)
        Цвет объекта в RGB палитре, каждый элемент принимает
        значение от 0 до 255.
        По умолчанию - цвет игрового поля.

    position : tuple(int, int)
        Позиция объекта на экране.
        По умолчанию - верхний левый угол.
    """

    def __init__(self, color=BOARD_BACKGROUND_COLOR, position=(0, 0)):
        self.body_color = color
        self.position = position

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Snake(GameObject):
    """Класс, описывающий игровой объект - змейку.

    Атрибуты
    --------------
    color : tuple(int, int, int)
        Цвет змейки в RGB палитре, каждый элемент принимает
        значение от 0 до 255.
        По умолчанию - цвет змейки.

    positions : list(tuple(int, int), ...)
        Позиции элементов змейки на экране.
        По умолчанию - список с одной координатой в центре поля.

    direction : tuple(int, int)
        Направление змейки. Каждый элемент принимает значения от -1 до 1.
        По умолчанию - движение вправо (1, 0).

    next_direction : None or tuple(int, int)
        Следующее направление змейки. Необходимо для смены направления.
        По умолчанию - None.
    """

    def __init__(self, color=SNAKE_COLOR, positions=[(SNAKE_START_POSITION)],
                 direction=RIGHT, next_direction=None):
        super().__init__(color, positions[0])
        self.length = len(positions)
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = positions[-1]

    # Метод draw класса Snake
    def draw(self):
        """Метод для отрисовки змейки на экране"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Передвижение змейки
    def move(self):
        """Перемещение змейки в указанном направлении."""
        new_head_position = self.new_head_position()

        if len(self.positions) > 1:
            self.last = self.positions.pop()
            self.positions.insert(0, new_head_position)
        else:
            self.last = self.get_head_position()
            self.positions[0] = (new_head_position)

    # Возвращает новую позицию головы
    def new_head_position(self):
        """Метод, возваращающий новую позицию головы змейки.
        Необходим для метода move().
        """
        x_pos = self.get_head_position()[0]
        y_pos = self.get_head_position()[1]

        x_pos += self.direction[0] * GRID_SIZE
        y_pos += self.direction[1] * GRID_SIZE

        if x_pos > SCREEN_WIDTH - GRID_SIZE:
            x_pos = 0
        elif x_pos < 0:
            x_pos = SCREEN_WIDTH - GRID_SIZE
        elif y_pos > SCREEN_HEIGHT - GRID_SIZE:
            y_pos = 0
        elif y_pos < 0:
            y_pos = SCREEN_HEIGHT - GRID_SIZE

        new_head_position = (x_pos, y_pos)

        return new_head_position

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Возвращает позицию головы
    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    # В случае самопересечения "обрезает" змейку по уши
    def reset(self):
        """Возвращает змейку в начальное состояние в случае самопересечения."""
        self.remove_dead_snake()
        self.positions = [self.get_head_position()]
        self.draw()
        self.length = 1

    # Метод для затирания следов змейки после самопересечения
    def remove_dead_snake(self):
        """Метод, стирающий 'остатки' змейки после возвращения
        в начальное состояние.
        """
        for element in self.positions[1:]:
            rect = pygame.Rect(element, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """Класс яблока - еды для змейки.

    Атрибуты
    --------------
    color : tuple(int, int, int)
        Цвет объекта в RGB палитре, каждый элемент принимает
        значение от 0 до 255.
        По умолчанию - цвет яблока.

    position : tuple(int, int)
        Позиция объекта на экране.
        По умолчанию - верхний левый угол.
    """

    def __init__(self, color=APPLE_COLOR, position=(0, 0)):
        super().__init__(color, position)
        self.position = position

    # Метод draw класса Apple
    def draw(self):
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Выбирает случайную позицию яблока из доступных позиций
    def randomize_position(self, not_possible_positions):
        """Метод, возвращающий случайную позицию яблока
        и исключающий неверные позиции.

        Параметры
        --------------
        not_possible_positions - недопустимые позиции.
        """
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (position_x, position_y)
            if position in not_possible_positions:
                continue
            self.position = (position_x, position_y)
            break


# Функция обработки действий пользователя
def handle_keys(game_object: Snake):
    """Функция для обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Функция обработки действий пользователя
def update_title(max_length, length=1):
    max_length = max(max_length, length)
    pygame.display.set_caption(f'Змейка - {max_length}')
    return max_length


def main():
    """Главная функция программы."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.

    snake = Snake()
    max_length = snake.length
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake_head = snake.get_head_position()
        apple.draw()
        snake.draw()

        if snake_head in snake.positions[2:]:
            snake.reset()

        if snake_head == apple.position:
            snake.positions.insert(0, apple.position)
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw()
            max_length = update_title(max_length, snake.length)

        pygame.display.update()


if __name__ == '__main__':
    main()
