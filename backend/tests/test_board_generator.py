import pytest
from app.game.board_generator import BoardGenerator

def test_board_generator_initialization():
    generator = BoardGenerator()
    assert generator.valid_sizes[36] == (6, 6)
    assert generator.valid_sizes[100] == (10, 10)

def test_find_valid_board_size():
    generator = BoardGenerator()
    assert generator._find_valid_board_size(35) == 36
    assert generator._find_valid_board_size(36) == 36
    assert generator._find_valid_board_size(37) == 42
    assert generator._find_valid_board_size(101) is None

def test_board_generation_with_lengths():
    generator = BoardGenerator()
    # Using the same test case from wormtest.py that we know works
    lengths = [10, 15, 11]  # sum = 36, fits in 6x6 board
    
    board, placement_info = generator.generate_board_with_lengths(lengths)
    
    # Print the board for visualization
    print("\nGenerated board:")
    for row in board:
        print(" ".join(f"{cell:2}" for cell in row))
    print("\nPaths:")
    for i, path in enumerate(placement_info['paths']):
        print(f"Path {i+1} (length {lengths[i]}): {path}")
    
    # Check board dimensions
    assert len(board) == 6  # Should be 6x6 for 36 letters
    assert len(board[0]) == 6
    
    # Verify all paths are placed and have correct lengths
    paths = placement_info['paths']
    assert len(paths) == len(lengths)
    
    # Verify each path has the correct length
    for path, expected_length in zip(paths, lengths):
        assert len(path) == expected_length
    
    # Verify paths don't overlap
    all_positions = set()
    for path in paths:
        for pos in path:
            assert pos not in all_positions, "Paths should not overlap"
            all_positions.add(pos)
    
    # Verify board is completely filled
    for row in board:
        for cell in row:
            assert isinstance(cell, int) and cell > 0, "Each cell should contain a positive integer representing the worm ID" 

def test_board_generation_with_words():
    generator = BoardGenerator()
    # Using words that sum to 36 letters (6x6 board)
    words = [
        "STARLIGHT",  # 9 letters
        "MOONBEAMS",  # 9 letters
        "SUNRAYS",    # 7 letters
        "GLOW",       # 4 letters
        "DARK",       # 4 letters
        "SET"         # 3 letters
    ]  # Total: 9 + 9 + 7 + 4 + 4 + 3 = 36 letters
    
    board, placement_info = generator.generate_board_with_words(words)
    
    # Print the board for visualization
    print("\nGenerated board:")
    for row in board:
        print(" ".join(f"{cell:2}" for cell in row))
    print("\nPaths and Words:")
    for i, (word, path) in enumerate(zip(words, placement_info['paths'])):
        print(f"Word {i+1} ({word}, length {len(word)}): {path}")
        # Verify the word is correctly placed along the path
        word_on_board = ""
        for r, c in path:
            word_on_board += board[r][c]
        assert word_on_board == word, f"Word {word} not correctly placed on board, found {word_on_board}"
    
    # Check board dimensions
    assert len(board) == 6  # Should be 6x6 for 36 letters
    assert len(board[0]) == 6
    
    # Verify all paths are placed and have correct lengths
    paths = placement_info['paths']
    assert len(paths) == len(words)
    
    # Verify each path has the correct length
    for path, word in zip(paths, words):
        assert len(path) == len(word)
    
    # Verify paths don't overlap
    all_positions = set()
    for path in paths:
        for pos in path:
            assert pos not in all_positions, "Paths should not overlap"
            all_positions.add(pos)
    
    # Verify board is completely filled with letters
    for row in board:
        for cell in row:
            assert cell.isalpha(), "Each cell should contain a letter" 