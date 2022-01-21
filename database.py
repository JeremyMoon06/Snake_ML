import copy
import json
from databaseConnection import db


import neuralNetwork
from game import current_game


def save_gameplay():
    file = open('dna_data.json')
    dna_list = json.load(file)
    file.close()
    my_cursor = db.cursor()
    my_cursor.execute('DROP TABLE IF EXISTS Gameplay_results')
    my_cursor.execute("CREATE TABLE Gameplay_results (database_iteration int, gameplay_list JSON)")
    database_iteration = 0
    for dna in dna_list:
        database_iteration += 1
        json_string = json.dumps(get_best_run(dna))
        my_cursor.execute("INSERT INTO Gameplay_results (database_iteration, gameplay_list) VALUES (%s, %s)",
                          (database_iteration, json_string))
        print(f'Generation {database_iteration} gameplay processed...')
    db.commit()


def get_best_run(dna):
    gameplay_list = []
    for _ in range(5):
        best_gameplay = []
        best_score = -1
        for _ in range(10):
            board = copy.deepcopy(current_game.board)
            board = convert_board(board)
            current_list_of_boards = [board]
            while not current_game.lose and not current_game.won:
                current_game.move(neuralNetwork.get_move(dna))
                board = copy.deepcopy(current_game.board)
                board = convert_board(board)
                current_list_of_boards.append(copy.deepcopy(board))
            if current_game.score > best_score:
                best_gameplay = current_list_of_boards
                best_score = current_game.score
            current_game.reset()
        gameplay_list.append(best_gameplay)
    return gameplay_list


def convert_board(board: []):
    board.pop(current_game.max_y - 1)
    board.pop(0)
    for board_row in board:
        board_row.pop(current_game.max_x - 1)
        board_row.pop(0)
    return board


save_gameplay()
