
import random
import os

STATS_DIR = "game_stats"
STATS_FILE = os.path.join(STATS_DIR, "stats.txt")

if not os.path.exists(STATS_DIR):
    os.makedirs(STATS_DIR)

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        f.write("Статистика игр:\n")

def save_stats(result):
    with open(STATS_FILE, "a", encoding="utf-8") as f:
        f.write(result + "\n")


def create_board(size):
    return [[" " for _ in range(size)] for _ in range(size)]


def print_board(board):
    print("\n   " + "  ".join(str(i) for i in range(len(board))))
    for i, row in enumerate(board):
        print(i, "| " + " | ".join(row) + " |")
    print()


def check_win(board, player):
    size = len(board)

    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(size):
        if all(board[row][col] == player for row in range(size)):
            return True

 
    if all(board[i][i] == player for i in range(size)):
        return True

    if all(board[i][size - i - 1] == player for i in range(size)):
        return True

    return False


def check_draw(board):
    return all(cell != " " for row in board for cell in row)


def play_game():

    while True:
        try:
            size = int(input("Введите размер поля (например 3): "))
            if size < 3:
                print("Размер должен быть минимум 3.")
                continue
            break
        except ValueError:
            print("Ошибка! Введите число.")

    board = create_board(size)

    current_player = random.choice(["X", "O"])
    print(f"\nПервым ходит: {current_player}")

    while True:
        print_board(board)

        print(f"Ход игрока {current_player}")

  
        try:
            row = int(input("Введите номер строки: "))
            col = int(input("Введите номер столбца: "))
        except ValueError:
            print("Ошибка! Введите числа.")
            continue

        if not (0 <= row < size and 0 <= col < size):
            print("Координаты вне поля!")
            continue

        if board[row][col] != " ":
            print("Клетка занята!")
            continue

        board[row][col] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Игрок {current_player} победил!")
            save_stats(f"Победил игрок {current_player}")
            break

        if check_draw(board):
            print_board(board)
            print("Ничья!")
            save_stats("Ничья")
            break

        current_player = "O" if current_player == "X" else "X"

def main():
    print("Крестики-нолики")
    print("Статистика сохраняется в папку game_stats\n")

    while True:
        play_game()

        again = input("Хотите начать новую игру? (да/нет): ").strip().lower()
        if again != "да":
            print("Выход из приложения.")
            break


if name == "main":

    main()
