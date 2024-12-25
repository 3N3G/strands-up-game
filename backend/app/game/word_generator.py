from typing import Dict, Set, List
import os
from abc import ABC, abstractmethod
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

class BaseWordGenerator(ABC):
    """Abstract base class for word generators."""
    def __init__(self):
        self.valid_sizes = {36, 42, 48, 49, 54, 56, 60, 63, 64, 70, 72, 77, 80, 81, 90, 100}

    @abstractmethod
    def generate_completion(self, prompt: str) -> str:
        """Generate a completion from the LLM."""
        pass

    def generate_word_set(self, seed_word: str = None) -> Dict[str, str]:
        """Generate a themed set of words for the game."""
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                prompt = self._create_prompt(seed_word, attempt > 0)
                print(f"Attempt {attempt + 1}: Sending prompt to LLM")
                
                response = self.generate_completion(prompt)
                print(f"Raw LLM response: {response}")
                
                result = self._parse_response(response)
                print(f"Parsed result: {result}")
                
                # Validate total letter count
                total_letters = len(result['special_word']) + sum(len(word) for word in result['words'])
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
Please help me create an educational word definition and wordplay puzzle with the following specifications:

GRID REQUIREMENTS:
1. Total letter count (all words combined including special word) must be exactly one of: 36, 42, 48, 49, 54, 56, 60, 63, 64, 70, 72, 77, 80, 81, 90, or 100 letters
2. Include 5-7 regular words plus one special longer word
3. The special word should be 8-15 letters (can be two words)
4. Regular words should be 3-8 letters each
5. All words should connect to one central theme

THEME GUIDELINES:
1. Create an educational or entertaining theme 
2. Make the theme specific and engaging
3. Choose words that are interesting discoveries
4. All words should clearly connect to the theme
5. Use grade-appropriate vocabulary

Example Format:
Theme: Not your average fruit stand
Special Word: tropicalfruit
Words: kiwi, mango, guava, papaya, lychee, fig
[Total: 42 letters]

More Examples:
Theme: In the Garden
Special Word: gardenherbs
Words: coriander, mint, basil, rosemary, thyme, parsley
[Total: 49 letters]

Theme: Out of this world
Special Word: telescopesights
Words: moon, mars, venus, jupiter, saturn, mercury
[Total: 48 letters]

Theme: Time for a change
Special Word: clockworks
Words: gear, dial, hands, tick, chime, wind
[Total: 36 letters]

Please provide:
Theme: [educational theme]
Special Word: [thematic word 8-15 letters]
Words: [5-7 related words]"""
        
        if is_retry:
            base_prompt += "\n\nPrevious words didn't match required letter counts. Please try again with words that sum to one of the valid total sizes."
        
        if seed_word:
            base_prompt += f"\n\nPlease use this word as inspiration for the theme: {seed_word}"
            
        return base_prompt

    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into structured data."""
        try:
            lines = response.strip().split('\n')
            result = {}
            
            for line in lines:
                if line.startswith('Theme:'):
                    result['theme'] = line.replace('Theme:', '').strip()
                elif line.startswith('Special Word:'):
                    result['special_word'] = line.replace('Special Word:', '').strip()
                elif line.startswith('Words:'):
                    words = line.replace('Words:', '').strip()
                    result['words'] = [w.strip() for w in words.split(',')]
            
            # Validate the response
            if not all(key in result for key in ['theme', 'special_word', 'words']):
                raise ValueError("Invalid response format from LLM")
            
            # Additional validation
            if len(result['special_word']) < 8:
                raise ValueError(f"Special word '{result['special_word']}' is too short (must be at least 8 letters)")
            
            if len(result['words']) < 5:
                raise ValueError(f"Not enough theme words (got {len(result['words'])}, need at least 5)")
            
            return result
            
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")  # Log the error
            raise Exception(f"Failed to parse LLM response: {str(e)}")

class AnthropicWordGenerator(BaseWordGenerator):
    """Word generator using Anthropic's Claude API."""
    def __init__(self, api_key: str = None):
        super().__init__()
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and ANTHROPIC_API_KEY environment variable is not set")
        self.client = Anthropic(api_key=api_key)

    def generate_completion(self, prompt: str) -> str:
        """Generate a completion using Anthropic's Claude API."""
        response = self.client.completions.create(
            prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
            model="claude-2.1",
            max_tokens_to_sample=1024,
            stop_sequences=[HUMAN_PROMPT]
        )
        return response.completion

# Example of how to add a new LLM implementation:
"""
class OpenAIWordGenerator(BaseWordGenerator):
    def __init__(self, api_key: str = None):
        super().__init__()
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)

    def generate_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content
"""

# Default to Anthropic for now
WordGenerator = AnthropicWordGenerator