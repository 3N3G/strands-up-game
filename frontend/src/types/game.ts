export type Position = [number, number];

export type WordPlacement = {
    word: string;
    path: Position[];
};

export type PlacementInfo = {
    spangram: WordPlacement;
    words: WordPlacement[];
};

export type GameState = {
    theme: string;
    spangram: string;
    words: string[];
    board: string[][];
    placement_info: PlacementInfo;
}; 