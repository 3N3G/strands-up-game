import React from 'react';
import { ChakraProvider, Box, Heading, Text, VStack } from '@chakra-ui/react';
import GameContainer from './components/GameContainer';
import theme from './theme';

const App: React.FC = () => {
    return (
        <ChakraProvider theme={theme}>
            <Box minH="100vh" bg="gray.50">
                <VStack spacing={8} py={8}>
                    <Box textAlign="center">
                        <Heading size="2xl" mb={4}>
                            Word Search Game
                        </Heading>
                        <Text fontSize="lg" color="gray.600">
                            Find all the words hidden in the grid, including the special word!
                        </Text>
                    </Box>
                    <GameContainer />
                </VStack>
            </Box>
        </ChakraProvider>
    );
};

export default App;
