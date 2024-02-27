import requests

def generate_sudoku():
    response = requests.get('https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{solution}}}')
    sudoku = response.json()["newboard"]["grids"][0]["solution"]
    return sudoku


def main():
    print(generate_sudoku())


main()