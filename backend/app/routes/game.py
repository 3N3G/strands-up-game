from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from ..game.word_generator import WordGenerator
from ..game.board_generator import BoardGenerator

router = APIRouter()
board_generator = BoardGenerator()

class GameResponse(BaseModel):
    theme: str
    spangram: str
    words: List[str]
    board: List[List[str]]
    placement_info: Dict

class GameRequest(BaseModel):
    seed_word: Optional[str] = None

@router.post("/generate", response_model=GameResponse)
async def generate_game(request: GameRequest):
    try:
        # Initialize word generator with Anthropic API
        word_generator = WordGenerator(api_provider="anthropic")
        
        # Generate words
        word_set = word_generator.generate_word_set(request.seed_word)
        
        # Generate board
        board, placement_info = board_generator.generate_board(
            word_set['spangram'],
            word_set['words']
        )
        
        return GameResponse(
            theme=word_set['theme'],
            spangram=word_set['spangram'],
            words=word_set['words'],
            board=board,
            placement_info=placement_info
        )
        
    except Exception as e:
        # Log the actual error for debugging but don't send it to the client
        print(f"Error generating game: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Unable to generate game. Please try again."
        ) 