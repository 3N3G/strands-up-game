import React, { useState, useEffect } from 'react';
import {
    Grid,
    GridItem,
    VStack,
    Text,
    Box,
    useToast,
    HStack,
    Button,
    IconButton,
} from '@chakra-ui/react';
import { PlacementInfo } from '../types/game';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

interface GameBoardProps {
    board: string[][];
    words: string[];
    special_word: string;
    placementInfo: PlacementInfo;
}

type Position = [number, number];

export const GameBoard: React.FC<GameBoardProps> = ({
    board,
    words,
    special_word,
    placementInfo,
}) => {
    const [selectedCells, setSelectedCells] = useState<Position[]>([]);
    const [foundWords, setFoundWords] = useState<Set<string>>(new Set());
    const [foundPaths, setFoundPaths] = useState<Set<string>>(new Set());
    const [showWordList, setShowWordList] = useState<boolean>(true);
    const toast = useToast();

    // Clear state when a new game is generated
    useEffect(() => {
        setSelectedCells([]);
        setFoundWords(new Set());
        setFoundPaths(new Set());
    }, [board]); // board prop changes when a new game is generated

    // Check if two cells are adjacent (including diagonals)
    const isAdjacent = (pos1: Position, pos2: Position): boolean => {
        const [row1, col1] = pos1;
        const [row2, col2] = pos2;
        const rowDiff = Math.abs(row1 - row2);
        const colDiff = Math.abs(col1 - col2);
        return rowDiff <= 1 && colDiff <= 1 && !(rowDiff === 0 && colDiff === 0);
    };

    // Convert path to string for Set storage
    const pathToString = (path: Position[]): string => {
        return path.map(([r, c]) => `${r},${c}`).join('|');
    };

    const handleCellClick = (row: number, col: number) => {
        const clickedPos: Position = [row, col];
        
        // If clicking the same cell as last selection, check the word
        if (selectedCells.length > 0) {
            const lastCell = selectedCells[selectedCells.length - 1];
            if (lastCell[0] === row && lastCell[1] === col) {
                checkForWord(selectedCells);
                return;
            }
        }
        
        // If clicking a non-adjacent cell or cell is part of a found word, clear selection
        if (
            selectedCells.length > 0 &&
            (!isAdjacent(selectedCells[selectedCells.length - 1], clickedPos) ||
            foundPaths.has(`${row},${col}`))
        ) {
            setSelectedCells([]);
            return;
        }
        
        // Add the cell to selection
        setSelectedCells([...selectedCells, clickedPos]);
    };

    const checkForWord = (cells: Position[]) => {
        const selectedWord = cells
            .map(([row, col]) => board[row][col])
            .join('');

        // Check if this path matches any word's path
        const pathStr = pathToString(cells);
        const allPlacements = [
            { word: special_word, path: placementInfo.special_word.path },
            ...placementInfo.words.map(w => ({ word: w.word, path: w.path }))
        ];

        const foundPlacement = allPlacements.find(({ word, path }) => {
            const correctPathStr = pathToString(path);
            return (
                word.toLowerCase() === selectedWord.toLowerCase() &&
                (pathStr === correctPathStr || pathStr === correctPathStr.split('|').reverse().join('|'))
            );
        });

        if (foundPlacement && !foundWords.has(foundPlacement.word)) {
            // Mark word as found
            const newFoundWords = new Set(foundWords);
            newFoundWords.add(foundPlacement.word);
            setFoundWords(newFoundWords);

            // Mark cells as found
            const newFoundPaths = new Set(foundPaths);
            cells.forEach(([r, c]) => newFoundPaths.add(`${r},${c}`));
            setFoundPaths(newFoundPaths);

            toast({
                title: 'Word Found!',
                description: foundPlacement.word === special_word 
                    ? 'Congratulations! You found the special word!' 
                    : `You found "${foundPlacement.word}"!`,
                status: 'success',
                duration: 2000,
                isClosable: true,
            });

            if (newFoundWords.size === allPlacements.length) {
                toast({
                    title: 'Congratulations!',
                    description: 'You found all the words!',
                    status: 'success',
                    duration: 5000,
                    isClosable: true,
                });
            }
        } else {
            // Only show "Try again" message if some cells were selected
            if (cells.length > 0) {
                toast({
                    title: 'Try again!',
                    status: 'info',
                    duration: 1000,
                    isClosable: true,
                });
            }
        }

        setSelectedCells([]);
    };

    const getCellStyle = (row: number, col: number) => {
        const isSelected = selectedCells.some(([r, c]) => r === row && c === col);
        const isFound = foundPaths.has(`${row},${col}`);
        
        if (isFound) return { bg: 'green.200', cursor: 'not-allowed', _hover: { bg: 'green.200' } };
        if (isSelected) return { bg: 'blue.200', cursor: 'pointer', _hover: { bg: 'blue.300' } };
        return { bg: 'gray.100', cursor: 'pointer', _hover: { bg: 'blue.100' } };
    };

    return (
        <VStack spacing={6} align="stretch">
            <Grid
                templateColumns={`repeat(${board[0].length}, 40px)`}
                gap={1}
                mx="auto"
            >
                {board.map((row, rowIndex) =>
                    row.map((cell, colIndex) => (
                        <GridItem
                            key={`${rowIndex}-${colIndex}`}
                            w="40px"
                            h="40px"
                            display="flex"
                            alignItems="center"
                            justifyContent="center"
                            borderRadius="md"
                            onClick={() => !foundPaths.has(`${rowIndex},${colIndex}`) && handleCellClick(rowIndex, colIndex)}
                            transition="background-color 0.2s"
                            {...getCellStyle(rowIndex, colIndex)}
                        >
                            <Text fontSize="lg" fontWeight="bold">
                                {cell}
                            </Text>
                        </GridItem>
                    ))
                )}
            </Grid>

            <Box>
                <HStack justify="space-between" align="center" mb={2}>
                    <Text fontWeight="bold">
                        Words Found: {foundWords.size}/{words.length + 1}
                    </Text>
                    <IconButton
                        aria-label={showWordList ? "Hide word list" : "Show word list"}
                        icon={showWordList ? <FaEyeSlash /> : <FaEye />}
                        onClick={() => setShowWordList(!showWordList)}
                        size="sm"
                        variant="ghost"
                    />
                </HStack>
                {showWordList && (
                    <HStack spacing={2} flexWrap="wrap" justify="center">
                        {[...words, special_word].map((word) => (
                            <Text
                                key={word}
                                px={2}
                                py={1}
                                borderRadius="md"
                                bg={foundWords.has(word) ? 'green.100' : 'gray.100'}
                                textDecoration={foundWords.has(word) ? 'line-through' : 'none'}
                                fontSize="sm"
                            >
                                {word}
                                {word === special_word && ' (special word)'}
                            </Text>
                        ))}
                    </HStack>
                )}
            </Box>
        </VStack>
    );
}; 