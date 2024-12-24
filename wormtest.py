import random
from typing import List, Tuple

def generate_worm_partition_advanced(lengths: List[int]) -> None:
    """
    Attempt to fully partition an m x n grid (with m,n in [6..10]) where sum(lengths) = m*n,
    into w worms. Each worm is a path of length=lengths[i], contiguous by edge or corner.

    This version uses global backtracking: if we fail to place worm i, we remove or 'undo'
    previous worm placements before trying other options.

    The final partition is printed, with each cell labeled by the worm ID index + 1.
    """

    total_squares = sum(lengths)
    valid_pairs = [
        (r, c)
        for r in range(6, 11)
        for c in range(6, 11)
        if r * c == total_squares
    ]
    if not valid_pairs:
        raise ValueError(f"No (m, n) in range [6..10]x[6..10] satisfies total squares={total_squares}.")

    # Attempt each valid dimension until we find a valid partition
    random.shuffle(valid_pairs)  # so we try them in random order
    for (m, n) in valid_pairs:
        board_worm_id = [[-1 for _ in range(n)] for _ in range(m)]
        # We'll track how many cells are filled
        filled_count = 0

        # Prepare adjacency offsets (8 possible directions)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
            """Return valid adjacent neighbors for cell (r,c)."""
            result = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    result.append((nr, nc))
            return result

        # Sort worms by descending length (often helps place big worms first)
        worms_ordered = sorted(enumerate(lengths), key=lambda x: x[1], reverse=True)

        def place_all_worms(worm_index: int) -> bool:
            """Try to place worm_index-th worm (in worms_ordered). If all placed, return True."""
            if worm_index == len(worms_ordered):
                return True  # all worms placed successfully

            idx, length = worms_ordered[worm_index]
            # Attempt to place this worm in a path of 'length' squares
            # We'll try each free cell as a potential start
            free_cells = [
                (r, c)
                for r in range(m)
                for c in range(n)
                if board_worm_id[r][c] == -1
            ]
            random.shuffle(free_cells)

            for start_cell in free_cells:
                path = [start_cell]
                if build_worm_path(path, length):
                    # Mark the path with this worm index
                    for (rr, cc) in path:
                        board_worm_id[rr][cc] = idx
                    # Recurse for next worm
                    if place_all_worms(worm_index + 1):
                        return True
                    else:
                        # Undo if it didn't work out
                        for (rr, cc) in path:
                            board_worm_id[rr][cc] = -1
            return False

        def build_worm_path(path: List[Tuple[int, int]], target_length: int) -> bool:
            """
            Recursively extend a path by adjacent squares (edge or corner).
            If we reach target_length, success -> True.
            Otherwise, try neighbors of the last cell in path.
            """
            if len(path) == target_length:
                return True

            (r, c) = path[-1]
            # Shuffle neighbors for random exploration
            neighs = neighbors(r, c)
            random.shuffle(neighs)
            for (nr, nc) in neighs:
                if board_worm_id[nr][nc] == -1 and (nr, nc) not in path:
                    path.append((nr, nc))
                    if build_worm_path(path, target_length):
                        return True
                    path.pop()

            return False

        # Try to place all worms with global backtracking
        if place_all_worms(0):
            # We succeeded for this dimension, print and return
            print(f"Successfully partitioned {m}x{n} board into {len(lengths)} worms.")
            # Print the result, each cell as worm_id + 1
            for row in range(m):
                row_str = " ".join(f"{board_worm_id[row][col]+1:02d}" for col in range(n))
                print(row_str)
            return

    # If we arrive here, no dimension or partition succeeded
    raise RuntimeError("Failed to generate a valid worm partition after trying all dimensions.")


def demo():
    # Example usage:
    # Suppose we have 3 worms with lengths that sum to 36 (6x6).
    # Expand or modify as needed.
    lengths = [10, 15, 11]  # sum=36
    generate_worm_partition_advanced(lengths)