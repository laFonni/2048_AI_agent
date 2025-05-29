import time
from agent import ExpectimaxAgent
from game2048 import Game2048

def print_board(board):
    for row in board:
        print(" | ".join(f"{val:4}" if val != 0 else "    " for val in row))
    print()

def evaluate_agent(num_trials=50, max_depth=4):
    results = []
    agent = ExpectimaxAgent(max_depth=max_depth)

    for i in range(num_trials):
        game = Game2048()
        moves = 0
        start_time = time.time()


        while not game.is_game_over():
            move = agent.get_move(game)
            if move is None:
                break
            game.move_with_cache(move)

            moves += 1

            # print(f"Move {moves}: {move.upper()}")
            # print_board(game.board)

        end_time = time.time()
        result = {
            'trial': i + 1,
            'max_tile': game.get_max_tile(),
            'score': game.get_score(),
            'moves': moves,
            'duration': round(end_time - start_time, 2)
        }
        results.append(result)

        print(f"Trial {i+1}: Max Tile = {result['max_tile']}, "
              f"Score = {result['score']}, Moves = {moves}, Time = {result['duration']}s")
        print("Final board:")
        print_board(game.board)

    return results
