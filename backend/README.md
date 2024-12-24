# Word Search Game Backend

This is the backend service for the Word Search Game, built with FastAPI and Python. It provides APIs for generating themed word search puzzles with a special "spangram" word that touches opposite sides of the board.

## Features

- Dynamic word and theme generation using OpenAI's GPT model
- Automatic board generation with word placement
- RESTful API endpoints
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

## Setup

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit the `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
- Root endpoint
- Returns: `{"message": "Word Search Game API is running"}`

### GET /health
- Health check endpoint
- Returns: `{"status": "healthy"}`

### POST /api/game/generate
- Generates a new word search game
- Request body:
  ```json
  {
    "seed_word": "optional_seed_word"
  }
  ```
- Returns:
  ```json
  {
    "theme": "Generated theme",
    "spangram": "Special word",
    "words": ["word1", "word2", ...],
    "board": [["A", "B", ...], ...],
    "placement_info": {
      "spangram": {...},
      "words": [...]
    }
  }
  ```

## Running Tests

Run the test suite:
```bash
pytest
```

Note: You need to have the `OPENAI_API_KEY` environment variable set to run the full test suite.

## Development

The project structure is organized as follows:

```
backend/
├── app/
│   ├── game/
│   │   ├── word_generator.py
│   │   └── board_generator.py
│   ├── routes/
│   │   └── game.py
│   └── main.py
├── tests/
│   ├── test_api.py
│   ├── test_board_generator.py
│   └── test_word_generator.py
├── requirements.txt
└── README.md
``` 