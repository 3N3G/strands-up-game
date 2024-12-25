import React, { useState } from 'react';
import {
    VStack,
    HStack,
    Button,
    Input,
    Text,
    useToast,
    Box,
    Container,
} from '@chakra-ui/react';
import { generateGame } from '../services/api';
import { GameState } from '../types/game';
import { GameBoard } from './GameBoard';

const GameContainer: React.FC = () => {
    const [seedWord, setSeedWord] = useState('');
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const toast = useToast();

    const handleGenerateGame = async () => {
        setIsLoading(true);
        try {
            const newGameState = await generateGame(seedWord || undefined);
            setGameState(newGameState);
            setSeedWord('');
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Failed to generate game';
            toast({
                title: 'Error',
                description: errorMessage,
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
            console.error('Game generation error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Container maxW="container.lg" py={8}>
            <VStack spacing={6} align="stretch">
                <Box>
                    <HStack spacing={4}>
                        <Input
                            placeholder="Enter a seed word (optional)"
                            value={seedWord}
                            onChange={(e) => setSeedWord(e.target.value)}
                            maxW="300px"
                        />
                        <Button
                            colorScheme="blue"
                            onClick={handleGenerateGame}
                            isLoading={isLoading}
                            minW="150px"
                            px={6}
                        >
                            Generate Game
                        </Button>
                    </HStack>
                </Box>

                {gameState && (
                    <VStack spacing={4} align="stretch">
                        <Text fontSize="xl" fontWeight="bold">
                            Theme: {gameState.theme}
                        </Text>
                        <GameBoard
                            board={gameState.board}
                            words={gameState.words}
                            special_word={gameState.special_word}
                            placementInfo={gameState.placement_info}
                        />
                    </VStack>
                )}
            </VStack>
        </Container>
    );
};

export default GameContainer; 