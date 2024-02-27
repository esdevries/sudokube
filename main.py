import game

def main():
    sudoku_game = game.create_game()
    game.print_game(sudoku_game)
    print(game.pick_random_icons())


if __name__== "__main__":
    main()