import requests

def generate_sudoku():
    response = requests.get('https://sudoku-game-and-api.netlify.app/api/sudoku')
    sudoku = response.json()["data"]
    return sudoku


def match_colors_to_sudoku(sudokus):
    colors = ("red", "yellow", "blue", "white", "green", "orange")
    matched_sudokus = zip(colors, sudokus)
    return list(matched_sudokus)


def match_color_to_number(sudoku_game):
    color, sudoku = sudoku_game[0], sudoku_game[1]
    matched_sudoku = []
    for line in sudoku:
        matched_line = []
        for number in line:
            matched_line.append([color, number])
        matched_sudoku.append(matched_line)

    return matched_sudoku

def create_game():
    sudokus = []
    for _ in range(6):
        sudokus.append(generate_sudoku())
    
    color_matched = match_colors_to_sudoku(sudokus)
    full_matched_game = []
    for sudoku in color_matched:
        full_matched_game.append(match_color_to_number(sudoku))
    
    return full_matched_game


def print_game(sudokus):
    for sudoku in sudokus:
        for line in sudoku:
            print(line)