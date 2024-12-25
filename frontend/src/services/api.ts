import axios from 'axios';
import { GameState } from '../types/game';

const API_URL = 'http://localhost:8000/api';
const ANTHROPIC_API_KEY = import.meta.env.VITE_ANTHROPIC_API_KEY;

export const generateGame = async (seedWord?: string): Promise<GameState> => {
    try {
        if (!ANTHROPIC_API_KEY) {
            throw new Error('Anthropic API key is not configured');
        }

        const response = await axios.post(`${API_URL}/game/generate`, {
            seed_word: seedWord
        }, {
            headers: {
                'Authorization': `Bearer ${ANTHROPIC_API_KEY}`
            }
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