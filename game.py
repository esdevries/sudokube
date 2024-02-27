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


def convert2d(x, y):
    return (x+y*9)


def convert2dreverse(position):
    return (position % 9 ,position // 9)


def process_icon(svg_icon_path):
    svg_format = open_icon(svg_icon_path)
    root = ET.fromstring(svg_format)
    elements_with_fill = root.findall('.//*[@fill]')
    full_cords = {}

    def extract_coordinates(points):
        return [tuple(map(float, point.split(','))) for point in points.split()]

    for element in elements_with_fill:

        if element.get('points') != None:
            cords = extract_coordinates(element.get('points'))
            for cord in cords:
                try:
                    full_cords[int(convert2d(cord[0], cord[1]))] = element.get('fill')
                except ValueError:
                    print("Could not convert float coordinate to int")  
                    exit()

        elif element.get('x') != None:
            try:
                width = int(element.get('width', 1))
                height = int(element.get('height', 1))                
                base_x = int(element.get('x', 1))
                base_y = int(element.get('y', 1))
            except ValueError:
                print("Could not convert width and height to integers")
                exit()
            for wid in range(width):
                for heit in range(height):
                    full_cords[convert2d(base_x+wid,base_y+heit)] = element.get('fill')

    for position in range(81):
        if position not in full_cords.keys():
            full_cords[position] = '#FFFFFF'
    
    return full_cords


def generate_sudoku():
    response = requests.get('https://sudoku-game-and-api.netlify.app/api/sudoku')
    sudoku = response.json()["data"]
    return sudoku


def match_colors_to_sudokus(sudokus):
    full_sodoku_list = []

    random_icons = pick_random_icons()
    matching_sudok = list(zip(random_icons, sudokus))

    for sudoku_and_color in matching_sudok:
        sudoku = sudoku_and_color[1]
        print(sudoku_and_color)

        
    return full_sodoku_list

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
    
    color_matched = match_colors_to_sudokus(sudokus)
    full_matched_game = []
    for sudoku in color_matched:
        full_matched_game.append(match_color_to_number(sudoku))
    
    return full_matched_game


def print_game(sudokus):
    for sudoku in sudokus:
        for line in sudoku:
            print(line)