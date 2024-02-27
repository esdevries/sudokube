import requests
import os
import random
import xml.etree.ElementTree as ET


def pick_random_icons():
    all_icons = os.listdir('./icons')
    all_icons = [icon for icon in all_icons if os.path.isfile(os.path.join('./icons', icon))]
    return random.sample(all_icons, 6)


def open_icon(icon_path):
    try:
        with open(icon_path, 'r') as in_icon:
            return in_icon.read()
    except FileNotFoundError:
        print("Icon not found")
        exit()


def process_icon(svg_icon_path):
    svg_format = open_icon(svg_icon_path)
    root = ET.fromstring(svg_format)
    elements_with_fill = root.findall('.//*[@fill]')
    for element in elements_with_fill:
        print(element.get('points'), element.get('fill'))


def generate_sudoku():
    response = requests.get('https://sudoku-game-and-api.netlify.app/api/sudoku')
    sudoku = response.json()["data"]
    return sudoku


def match_colors_to_sudoku(sudokus):
    # process icon

    matched_sudokus = zip(colors, sudokus)
    return list(matched_sudokus)


def match_color_to_number(sudoku_game):
    color, sudoku = sudoku_game[0], sudoku_game[1]
    matched_sudoku = []
    for line in sudoku:
        matched_line = []
        for number in line:
            matched_line.append((color, number))
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