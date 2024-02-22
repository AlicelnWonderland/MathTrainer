import pygame
import random
import sys
import json

pygame.mixer.init()
background_music = pygame.mixer.Sound("music.mp3")
background_music.play(-1)

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1200, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тренажер математики")

font = pygame.font.SysFont("Comic Sans MS", 45)

class Leaderboard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.leaderboard = self.load_leaderboard()

    def load_leaderboard(self):
        try:
            with open(self.filename, "r") as f:
                leaderboard = json.load(f)
                if not isinstance(leaderboard, list):
                    leaderboard = []
        except (FileNotFoundError, json.JSONDecodeError):
            leaderboard = []
        return leaderboard

    def save_leaderboard(self):
        with open(self.filename, "w") as f:
            json.dump(self.leaderboard, f)

    def update_leaderboard(self, name, score):
        self.leaderboard.append({"name": name, "score": score})
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        if len(self.leaderboard) > 10:
            self.leaderboard = self.leaderboard[:10]
        self.save_leaderboard()

    def get_leaderboard(self):
        return self.leaderboard

leaderboard = Leaderboard()

def generate_math_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    problem = f"{num1} {operator} {num2}"
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    return problem, str(answer)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def get_user_name():
    background_image = pygame.image.load("background_image.png")
    screen.blit(background_image, (0, 0))
    draw_text("Введите ваше имя:", font, BLACK, 450, HEIGHT // 2 - 50)
    pygame.display.flip()
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        background_image = pygame.image.load("background_image.png")
        screen.blit(background_image, (0, 0))
        draw_text("Введите ваше имя:", font, BLACK, 425, 400)
        draw_text(name, font, BLACK, 520, 500)
        pygame.display.flip()
    return name

def main():
    name = get_user_name()

    clock = pygame.time.Clock()
    running = True
    correct_answers = 0
    total_questions = 0
    start_ticks = pygame.time.get_ticks()
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, 1000)

    problem, answer = generate_math_problem()
    user_answer = ""
    background_image = pygame.image.load("background_image.png")
    screen.blit(background_image, (0, 0))
    while running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if user_answer and (user_answer[0] != '-' or len(user_answer) > 1):
                        total_questions += 1
                        if int(user_answer) == int(answer):
                            correct_answers += 1
                    problem, answer = generate_math_problem()
                    user_answer = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.key == pygame.K_MINUS and not user_answer:
                    user_answer += event.unicode
                elif event.unicode.isdigit():
                    user_answer += event.unicode

            elif event.type == TIMEREVENT:
                pass


        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 20:
            running = False

        draw_text(problem, font, (0,0,255), 570, 455)
        draw_text("Ваш ответ: " + user_answer, font, (255,0,0), 430,550)
        timer = "Осталось времени: " + str(20 - int(seconds))
        draw_text(timer, font, (255,0,255), 390, 350)
        draw_text(f"Правильных ответов: {correct_answers}/{total_questions}", font, (0,128,0),350, 650)

        pygame.display.flip()
        clock.tick(30)

    leaderboard.update_leaderboard(name, correct_answers)
    leaderboard_scores = leaderboard.get_leaderboard()

    leaderboard_title_font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    leaderboard_score_font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)

    leaderboard_text = " "
    draw_text(leaderboard_text, leaderboard_title_font, (127,255,77), WIDTH // 2 - 150, HEIGHT // 10)

    leaderboard_y = HEIGHT // 5
    for i, entry in enumerate(leaderboard_scores, 1):
        score_text = f"{i}. {entry['name']}: {entry['score']}"
        draw_text(score_text, leaderboard_score_font, (127,255,77), WIDTH // 2 - 150, leaderboard_y + i * 55)

    background_image = pygame.image.load("leaderboard.png")
    screen.blit(background_image, (0, 0))
    draw_text(leaderboard_text, leaderboard_title_font, (127,255,77),WIDTH // 2 - 150, HEIGHT // 2 - 130 + 20)

    leaderboard_y = HEIGHT // 5
    for i, entry in enumerate(leaderboard_scores, 1):
        score_text = f"{i}. {entry['name']}: {entry['score']}"
        draw_text(score_text, leaderboard_score_font, (127,255,77), WIDTH // 2 - 150, leaderboard_y + i * 55)

    pygame.display.flip()
    running_leaderboard = True
    while running_leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_leaderboard = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_leaderboard = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
