export type Position = [number, number];

export type WordPlacement = {
    word: string;
    path: Position[];
};

export type PlacementInfo = {
    special_word: WordPlacement;
    words: WordPlacement[];
};

export type GameState = {
    theme: string;
    special_word: string;
    words: string[];
    board: string[][];
    placement_info: PlacementInfo;
}; 