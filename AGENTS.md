# Chicken Invaders - Agent Guide

## Run the app
```bash
cd /home/wajira/chiken_inveders
source venv/bin/activate
python3 app.py
```
App runs on port 6001 at http://127.0.0.1:6001

## Restart the app
```bash
fuser -k 6001/tcp 2>/dev/null
sleep 1
cd /home/wajira/chiken_inveders && source venv/bin/activate && nohup python3 app.py > /tmp/flask.log 2>&1 &
```

## Verify it's running
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:6001
```

## Project structure
- `app.py` - Flask server with API endpoints and score management
- `templates/index.html` - Single-page game (HTML + CSS + JS)
- `scores.json` - Persistent score storage
- `venv/` - Python virtual environment

## API endpoints
- `POST /api/score` - Submit a score `{name, score, level}`
- `GET /api/leaderboard` - Get all-time, daily, weekly leaderboards
- `POST /api/check_high` - Check if score qualifies `{score}` → `{is_high, reasons}`

## Key files
- `templates/index.html` - All game logic (canvas drawing, game loop, collision detection, sound via Web Audio API)
- `app.py` - All server logic (Flask routes, score persistence in JSON)

## Conventions
- No external JS/CSS libraries - pure HTML5 Canvas + vanilla JS
- Scores persist in `scores.json` (JSON file, not a database)
- Game runs at 60fps via `requestAnimationFrame`
- Sound effects via Web Audio API oscillator (square wave beeps)
