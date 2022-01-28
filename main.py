import pygame
import numpy as np
import random

################################# 초기 셋팅 ########################################
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

# 화면 크기 설정
screen_width = 450 # 가로 크기
screen_height = 305 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름
pygame.display.set_caption("2048_Game")

# 블럭 생성
block_limits = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
block_colors = dict()
block_colors[0] = (255, 255, 255)
for idx, i in enumerate(block_limits):
    block_colors[i] = (255-(15 * idx), 255-(15 * idx), 0)

block = pygame.Surface((70, 70))
best_score = 0

################################# 게임 사용 함수 ###################################
def make_random_block(matrix):
    temp = np.transpose(np.where(matrix==0))
    if len(temp) != 0:
        x, y = temp[random.randint(0, len(temp)-1)]
        matrix[x][y] = 2
    return matrix


def draw_matrix(screen, matrix):
    # 검은 배경
    screen.fill((0, 0, 0))
    # 채우기
    y = 5
    for i in range(4):
        x = 5
        for j in range(4):
            if matrix[i][j] != 0:
                if matrix[i][j] >= 256:
                    textsurface = myfont.render('{}'.format(matrix[i][j]), False, (255, 255, 255))
                else:
                    textsurface = myfont.render('{}'.format(matrix[i][j]), False, (0, 0, 0))
                font_w, _ = textsurface.get_size()
                block.fill(block_colors[matrix[i][j]])
                screen.blit(block, (x, y))
                screen.blit(textsurface, (x + 35 - font_w/2, y + 20))
            else:
                block.fill(block_colors[matrix[i][j]])
                screen.blit(block, (x, y))
            x += 75
        y += 75
    return screen

def draw_side(screen, score, best_score):
    # 최대값
    Score_text = myfont.render('Score', False, (255, 255, 255))
    screen.blit(Score_text, (315, 30))
    score_F = myfont.render('{}'.format(score), False, (255, 255, 255))
    screen.blit(score_F, (315, 60))

    # best_score
    Score_text = myfont.render('Best Score', False, (255, 255, 255))
    screen.blit(Score_text, (315, 90))
    best_score_F = myfont.render('{}'.format(best_score), False, (255, 255, 255))
    screen.blit(best_score_F, (315, 120))

    # Restart
    Restart_text = myfont.render('Restart', False, (255, 255, 255))
    screen.blit(Restart_text, (315, 230))
    PressR = myfont.render('Press Key \'r\'', False, (255, 255, 255))
    screen.blit(PressR, (315, 260))
    return screen

def play_game(matrix, direction, score):
    matrix = np.rot90(matrix, k=direction)
    for i in range(len(matrix)):
        temp = [element for element in matrix[i] if element != 0]
        change = list()
        prior = 0
        for element in temp:
            if element == prior:
                change.pop()
                change.append(element * 2)
                score += (element * 2)
                prior = 0
            else:
                change.append(element)
                prior = element
            matrix[i] = change + [0] * (len(matrix) - len(change))
    matrix = np.rot90(matrix, k=(4- direction))
    return np.array(matrix), score

def init(screen, best_score): # 초기화
    # 초기 매트릭스 생성
    matrix = np.zeros(shape=(16,), dtype=np.int16)
    select = random.sample(range(0, 15), 4)
    matrix[select] = 2
    matrix = np.reshape(matrix, (4,4))

    # 스코어 초기화
    score = 0

    # matrix 그리기
    screen = draw_matrix(screen, matrix)
    screen = draw_side(screen, score, best_score)

    return matrix, score, screen

# 하, 우
dx = [0, 1]
dy = [1, 0]
def is_lose(matrix):
    for i in range(4):
        for j in range(4):
            for move in range(2):
                temp_x = i + dy[move]
                temp_y = j + dx[move]
                if temp_x > 3 or temp_y > 3:
                    continue
                if matrix[i][j] == matrix[temp_x][temp_y] or matrix[temp_x][temp_y] == 0:
                    return True
    return False

################################# 게임 시작 ########################################
# 초기화
matrix, score, screen = init(screen, best_score)

# 게임 시작
running = True # 게임 실행 여부
while running:
    for event in pygame.event.get(): # 실행 중, 이벤트 발생시 이벤트 가져오기
        if event.type == pygame.QUIT: # X버튼을 눌러 종료시
            running = False
        if event.type == pygame.KEYDOWN: # 키가 눌렸을 때, 반대 KEYUP
            valid = 0 # 상, 하, 좌, 우 키에만 반응
            if event.key == pygame.K_LEFT: # 왼쪽 버튼
                matrix, score = play_game(matrix, 0, score)
                valid = 1
            elif event.key == pygame.K_RIGHT: # 오른쪽 버튼
                matrix, score = play_game(matrix, 2, score)
                valid = 1
            elif event.key == pygame.K_UP: # 위 버튼
                matrix, score = play_game(matrix, 1, score)
                valid = 1
            elif event.key == pygame.K_DOWN: # 아래 버튼
                matrix, score = play_game(matrix, 3, score)
                valid = 1
            elif event.key == pygame.K_r:
                matrix, score, screen = init(screen, best_score)
                continue

            if valid == 1:
                # 블록 생성
                matrix = make_random_block(matrix)
                # 키가 눌렸다면 화면 업데이트
                screen = draw_matrix(screen, matrix)
                best_score = max(score, best_score)
                screen = draw_side(screen, score, best_score)
                # 게임이 끝났는지 체크
                if not is_lose(matrix):
                    game_over_F = myfont.render('Game Over', False, (255, 0, 0))
                    screen.blit(game_over_F, (315, 150))


    pygame.display.update() # 게임화면을 계속 다시 그림

# 게임 종료
pygame.quit()