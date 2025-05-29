def summarize_results(results):
    num_games = len(results)
    total_score = sum(r['score'] for r in results)
    total_time = sum(r['duration'] for r in results)
    total_moves = sum(r['moves'] for r in results)
    max_tiles = [r['max_tile'] for r in results]

    summary = {
        'avg_score': round(total_score / num_games, 2),
        'avg_time': round(total_time / num_games, 2),
        'avg_moves': round(total_moves / num_games, 2),
        'max_tile_counts': {tile: max_tiles.count(tile) for tile in set(max_tiles)}
    }
    return summary

def print_summary(summary):
    print("\n--- Evaluation Summary ---")
    print(f"Average Score: {summary['avg_score']}")
    print(f"Average Time: {summary['avg_time']} seconds")
    print(f"Average Moves: {summary['avg_moves']}")
    print("Max Tile Frequencies:")
    for tile, count in sorted(summary['max_tile_counts'].items(), reverse=True):
        print(f"  {tile}: {count} games")
