from typing import List, Tuple, Optional, Dict, Set
import random
import logging
from collections import deque

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BoardGenerator:
    def __init__(self):
        self.valid_sizes = {
            36: (6, 6), 42: (6, 7), 48: (6, 8), 49: (7, 7),
            54: (6, 9), 56: (7, 8), 60: (6, 10), 63: (7, 9),
            64: (8, 8), 70: (7, 10), 72: (8, 9), 77: (7, 11),
            80: (8, 10), 81: (9, 9), 90: (9, 10), 100: (10, 10)
        }
        # 8 directions for adjacency (including diagonals)
        self.DIRECTIONS = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

    def generate_board(self, special_word: str, words: List[str]) -> Tuple[List[List[str]], dict]:
        """
        Generate a game board with the special word and theme words.
        The special word is treated as just another word for now, as the path-finding
        algorithm already handles placing longer words first.
        """
        # Combine special word and words
        all_words = [special_word] + words
        
        # Generate the board with words
        board, placement_info = self.generate_board_with_words(all_words)
        
        # Update placement info to separate special word from other words
        special_word_path = placement_info['paths'][0]  # First path is special word
        word_paths = placement_info['paths'][1:]    # Rest are theme words
        
        return board, {
            'special_word': {
                'word': special_word,
                'path': special_word_path
            },
            'words': [
                {'word': word, 'path': path}
                for word, path in zip(words, word_paths)
            ]
        }

    def _try_board_generation(self, rows: int, cols: int, special_word: str, words: List[str], word_lengths: List[Tuple[int, int]]) -> Tuple[List[List[str]], dict]:
        """Try to generate a board with the given words."""
        # Initialize empty board
        board = [['' for _ in range(cols)] for _ in range(rows)]
        placement_info = {'special_word': None, 'words': []}
        placed_positions: Set[Tuple[int, int]] = set()
        
        # Try to place each word
        all_words = [special_word] + words
        for word_idx, word_len in word_lengths:
            word = all_words[word_idx]
            logger.debug(f"Trying to place word: {word} (length {word_len})")
            
            # Try all possible starting positions
            placed = False
            empty_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in placed_positions]
            random.shuffle(empty_cells)
            
            for start_row, start_col in empty_cells:
                path = self._find_path_for_word(board, word, start_row, start_col, placed_positions)
                if path:
                    # Place the word along the path
                    self._place_word_along_path(board, word, path, placed_positions)
                    
                    # Record placement info
                    if word_idx == 0:  # special word
                        placement_info['special_word'] = {
                            'word': word,
                            'path': path
                        }
                    else:
                        placement_info['words'].append({
                            'word': word,
                            'path': path
                        })
                    placed = True
                    break
            
            if not placed:
                # Log the current board state for debugging
                logger.debug("Current board state:")
                for row in board:
                    logger.debug(" ".join(cell if cell else '.' for cell in row))
                raise ValueError(f"Could not place word '{word}'. Board is too constrained.")

        # Fill empty spaces with random letters
        self._fill_empty_spaces(board)
        return board, placement_info

    def _find_path_for_word(self, board: List[List[str]], word: str, start_row: int, start_col: int, placed_positions: Set[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        """Find a valid path for placing a word starting at the given position."""
        rows, cols = len(board), len(board[0])
        if start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols:
            return None

        # Use DFS instead of BFS for faster path finding
        def dfs(path: List[Tuple[int, int]], visited: Set[Tuple[int, int]], word_idx: int) -> Optional[List[Tuple[int, int]]]:
            if word_idx == len(word):
                return path

            current_row, current_col = path[-1]
            # Try each direction for the next letter
            directions = list(self.DIRECTIONS)
            random.shuffle(directions)  # Randomize direction order
            
            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc
                if (0 <= new_row < rows and 0 <= new_col < cols and 
                    (new_row, new_col) not in visited and
                    (new_row, new_col) not in placed_positions):
                    
                    # Check if this placement would be too close to other words
                    if self._is_valid_placement(board, new_row, new_col, visited, placed_positions):
                        new_path = path + [(new_row, new_col)]
                        new_visited = visited | {(new_row, new_col)}
                        result = dfs(new_path, new_visited, word_idx + 1)
                        if result:
                            return result
            return None

        # Try to find a path starting from the given position
        initial_path = [(start_row, start_col)]
        initial_visited = {(start_row, start_col)}
        return dfs(initial_path, initial_visited, 1)  # Start at index 1 since we're already placing the first letter

    def _is_valid_placement(self, board: List[List[str]], row: int, col: int, current_path: Set[Tuple[int, int]], placed_positions: Set[Tuple[int, int]]) -> bool:
        """Check if placing a letter at this position would be too close to other words."""
        rows, cols = len(board), len(board[0])
        
        # Check adjacent cells (including diagonals)
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            if (0 <= r < rows and 0 <= c < cols and 
                (r, c) in placed_positions and 
                (r, c) not in current_path):
                return False
        return True

    def _place_word_along_path(self, board: List[List[str]], word: str, path: List[Tuple[int, int]], placed_positions: Set[Tuple[int, int]]):
        """Place a word along the given path."""
        for i, (row, col) in enumerate(path):
            board[row][col] = word[i].upper()  # Convert to uppercase
            placed_positions.add((row, col))

    def _fill_empty_spaces(self, board: List[List[str]]):
        """Fill empty spaces with random letters."""
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == '':
                    board[i][j] = random.choice(letters)

    def _find_valid_board_size(self, total_letters: int) -> Optional[int]:
        """Find the smallest valid board size that can fit the given number of letters."""
        valid_sizes = sorted(self.valid_sizes.keys())
        for size in valid_sizes:
            if size >= total_letters:
                return size
        return None 

    def generate_board_with_lengths(self, lengths: List[int]) -> Tuple[List[List[int]], dict]:
        """
        Generate a board with paths of specified lengths.
        This is a simplified version that just places paths of given lengths,
        similar to the working wormtest.py implementation.
        """
        total_squares = sum(lengths)
        if total_squares not in self.valid_sizes:
            raise ValueError(f"Total squares {total_squares} must match a valid board size")

        rows, cols = self.valid_sizes[total_squares]
        board = [[-1 for _ in range(cols)] for _ in range(rows)]
        placement_info = {'paths': [None] * len(lengths)}  # Pre-allocate list to maintain order

        # Sort worms by descending length (helps place big worms first)
        worms_ordered = sorted(enumerate(lengths), key=lambda x: x[1], reverse=True)

        def place_all_worms(worm_index: int) -> bool:
            """Try to place worm_index-th worm. If all placed, return True."""
            if worm_index == len(worms_ordered):
                return True  # all worms placed successfully

            idx, length = worms_ordered[worm_index]
            # Try each free cell as a potential start
            free_cells = [
                (r, c)
                for r in range(rows)
                for c in range(cols)
                if board[r][c] == -1
            ]
            random.shuffle(free_cells)

            for start_cell in free_cells:
                path = [start_cell]
                if build_worm_path(path, length):
                    # Mark the path with this worm index
                    for (rr, cc) in path:
                        board[rr][cc] = idx + 1  # Use 1-based indices
                    placement_info['paths'][idx] = path  # Store path in original order
                    # Recurse for next worm
                    if place_all_worms(worm_index + 1):
                        return True
                    else:
                        # Undo if it didn't work out
                        for (rr, cc) in path:
                            board[rr][cc] = -1
                        placement_info['paths'][idx] = None
            return False

        def build_worm_path(path: List[Tuple[int, int]], target_length: int) -> bool:
            """
            Recursively extend a path by adjacent squares (edge or corner).
            If we reach target_length, success -> True.
            """
            if len(path) == target_length:
                return True

            (r, c) = path[-1]
            # Shuffle neighbors for random exploration
            neighbors = self._get_neighbors(r, c, rows, cols)
            random.shuffle(neighbors)
            
            for (nr, nc) in neighbors:
                if board[nr][nc] == -1 and (nr, nc) not in path:
                    path.append((nr, nc))
                    if build_worm_path(path, target_length):
                        return True
                    path.pop()
            return False

        # Try to place all worms with global backtracking
        if not place_all_worms(0):
            raise ValueError("Failed to generate a valid board with the given lengths")

        return board, placement_info

    def _get_neighbors(self, r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
        """Return valid adjacent neighbors for cell (r,c)."""
        result = []
        for dr, dc in self.DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                result.append((nr, nc))
        return result 

    def generate_board_with_words(self, words: List[str]) -> Tuple[List[List[str]], dict]:
        """
        Generate a board with the given words, placing each word along a contiguous path.
        This builds on top of generate_board_with_lengths by placing actual words along the paths.
        """
        # First get the paths using the lengths
        lengths = [len(word) for word in words]
        number_board, placement_info = self.generate_board_with_lengths(lengths)
        
        # Now create a new board for letters and place the words along the paths
        rows, cols = len(number_board), len(number_board[0])
        board = [['' for _ in range(cols)] for _ in range(rows)]
        
        # Place each word along its path
        for word, path in zip(words, placement_info['paths']):
            for i, (row, col) in enumerate(path):
                board[row][col] = word[i]
        
        # Fill empty spaces with random letters
        self._fill_empty_spaces(board)
        
        return board, placement_info 