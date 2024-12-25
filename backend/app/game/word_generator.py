from typing import Dict, Set
import os
from anthropic import Anthropic

class WordGenerator:
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and ANTHROPIC_API_KEY environment variable is not set")
        self.client = Anthropic(api_key=api_key)
        self.valid_sizes = {36, 42, 48, 49, 54, 56, 60, 63, 64, 70, 72, 77, 80, 81, 90, 100}

    def generate_word_set(self, seed_word: str = None) -> Dict[str, str]:
        """Generate a themed set of words for the game."""
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                prompt = self._create_prompt(seed_word, attempt > 0)
                print(f"Attempt {attempt + 1}: Sending prompt to LLM")
                
                response = self.client.messages.create(
                    model="claude-2.1",
                    max_tokens=1024,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                print(f"Raw LLM response: {response.content[0].text}")
                result = self._parse_response(response.content[0].text)
                print(f"Parsed result: {result}")
                
                # Validate total letter count
                total_letters = len(result['spangram']) + sum(len(word) for word in result['words'])
                print(f"Total letters: {total_letters}")
                
                if total_letters in self.valid_sizes:
                    return result
                else:
                    closest_size = min(self.valid_sizes, key=lambda x: abs(x - total_letters))
                    print(f"Invalid total letter count ({total_letters}). "
                          f"Closest valid size is {closest_size}. Retrying...")
                    continue
                
            except Exception as e:
                print(f"Error in word generation attempt {attempt + 1}: {str(e)}")
                if attempt == max_attempts - 1:
                    raise Exception(f"Failed to generate valid words after {max_attempts} attempts: {str(e)}")
                continue

    def _create_prompt(self, seed_word: str = None, is_retry: bool = False) -> str:
        """Create the prompt for the LLM."""
        base_prompt = """
You are a creative word search puzzle generator. Your task is to generate an engaging theme and set of words that will create an interesting and challenging puzzle.

CRITICAL REQUIREMENTS:
1. The total number of letters in ALL words (including the spangram) MUST equal one of these exact numbers: 36, 42, 48, 49, 54, 56, 60, 63, 64, 70, 72, 77, 80, 81, 90, or 100.
2. Generate 5-7 theme words plus one spangram.
3. The spangram must be 8-15 letters long and can be two words.
4. Theme words should be 3-8 letters each.
5. All words must cleverly relate to the theme.

CREATIVE GUIDELINES:
1. Instead of using the seed word directly as the theme, use it as inspiration to generate a more specific, surprising, or clever theme.
2. The theme should be intriguing and not immediately obvious - make players think!
3. The spangram should be a revealing or clever twist on the theme.
4. Choose theme words that have interesting connections to each other.
5. Avoid overly simple or common words - prefer words that are fun to discover.

Examples of creative themes:

Theme: Not your average fruit stand
Spangram: dragonfruits
Words: kiwi, mango, guava, papaya, lychee, fig
[Total: 42 letters - perfect for a 6x7 grid]

Theme: Sounds fishy to me
Spangram: underwater
Words: sonar, splash, bubble, wave, fins, dive
[Total: 36 letters - perfect for a 6x6 grid]

Theme: Time for a change
Spangram: clockworks
Words: gear, dial, hands, tick, chime, wind
[Total: 36 letters - perfect for a 6x6 grid]

Theme: Hidden in plain sight
Spangram: camouflage
Words: blend, hide, lurk, mask, cover, spot
[Total: 36 letters - perfect for a 6x6 grid]

Please provide:
Theme: [an intriguing theme that makes players curious]
Spangram: [a revealing or clever word that ties the theme together]
Words: [interesting, thematic words that create satisfying discoveries]
"""
        
        if is_retry:
            base_prompt += "\n\nPrevious attempt had incorrect letter count. Please try again with different words that sum to one of the valid total sizes."
        
        if seed_word:
            base_prompt += f"\n\nUse this word as creative inspiration (NOT necessarily the direct theme): {seed_word}"
            
        return base_prompt

    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into structured data."""
        try:
            lines = response.strip().split('\n')
            result = {}
            
            for line in lines:
                if line.startswith('Theme:'):
                    result['theme'] = line.replace('Theme:', '').strip()
                elif line.startswith('Spangram:'):
                    result['spangram'] = line.replace('Spangram:', '').strip()
                elif line.startswith('Words:'):
                    words = line.replace('Words:', '').strip()
                    result['words'] = [w.strip() for w in words.split(',')]
            
            # Validate the response
            if not all(key in result for key in ['theme', 'spangram', 'words']):
                raise ValueError("Invalid response format from LLM")
            
            # Additional validation
            if len(result['spangram']) < 8:
                raise ValueError(f"Spangram '{result['spangram']}' is too short (must be at least 8 letters)")
            
            if len(result['words']) < 5:
                raise ValueError(f"Not enough theme words (got {len(result['words'])}, need at least 5)")
            
            return result
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")  # Log the error
            raise Exception(f"Failed to parse LLM response: {str(e)}") 