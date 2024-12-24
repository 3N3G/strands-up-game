from wormtest import generate_worm_partition_advanced
import random

def visualize_board(board, m, n):
    """Visualize the current state of the board."""
    print("\nCurrent board state:")
    for r in range(m):
        row_str = " ".join(f"{board[r][c]:2}" if board[r][c] != -1 else " ." for c in range(n))
        print(row_str)
    print()

def test_word_partition(max_attempts=10):
    # Test case: A 6x6 board (36 squares) with different length distribution
    # Try more varied lengths: one very long worm (15), one medium (10), and one shorter (11)
    word_lengths = [15, 10, 11]  # still sums to 36
    
    print(f"Testing word partition with lengths: {word_lengths}")
    print(f"Sum of lengths: {sum(word_lengths)}")
    
    # Use current time for initial seed
    random.seed()
    
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        try:
            # Set a different random seed for each run
            random.seed()
            generate_worm_partition_advanced(word_lengths)
            print(f"\nTest passed on attempt {attempt + 1}!")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            continue
    
    print("\nAll attempts failed.")
    return False

if __name__ == "__main__":
    test_word_partition() 