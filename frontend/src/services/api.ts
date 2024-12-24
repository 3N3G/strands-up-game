import axios from 'axios';
import { GameState } from '../types/game';

const API_URL = 'http://localhost:8000/api';

export const generateGame = async (seedWord?: string): Promise<GameState> => {
    try {
        const response = await axios.post(`${API_URL}/game/generate`, {
            seed_word: seedWord
        });
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            const errorMessage = error.response?.data?.detail || 'Failed to generate game';
            console.error('Game generation error:', errorMessage);
            throw new Error(errorMessage);
        }
        throw error;
    }
}; 