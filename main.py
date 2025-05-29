from evaluate import evaluate_agent
from utils import summarize_results, print_summary
# from expectimax_agent import ExpectimaxAgent


if __name__ == "__main__":
    NUM_TRIALS = 50
    MAX_DEPTH = 6

    print(f"Running {NUM_TRIALS} games with Expectimax agent (depth={MAX_DEPTH})...\n")
    results = evaluate_agent(num_trials=NUM_TRIALS, max_depth=MAX_DEPTH)
    summary = summarize_results(results)
    print_summary(summary)
