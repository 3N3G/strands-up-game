# Word Search Game

A modern word search game with a twist! Find themed words and a special "spangram" word that connects opposite sides of the board.

## Features

- Dynamic word and theme generation using AI
- Interactive board with word path validation
- Real-time feedback and progress tracking
- Toggleable word list for different difficulty levels
- Responsive design for desktop and mobile

## Tech Stack

- Frontend:
  - React with TypeScript
  - Vite for build tooling
  - Chakra UI for components
  - React Icons

- Backend:
  - FastAPI (Python)
  - Anthropic Claude API for word generation
  - Custom board generation algorithm

## Setup

1. Clone the repository:
```bash
git clone https://github.com/3N3G/strands-up-game.git
cd strands-up-game
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Anthropic API key
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start the development servers:

Backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

The game will be available at http://localhost:5173

## Development

- Backend API runs on http://localhost:8000
- Frontend dev server runs on http://localhost:5173
- API documentation available at http://localhost:8000/docs

## Testing

Run backend tests:
```bash
cd backend
pytest
```

## License

MIT License - See LICENSE file for details 