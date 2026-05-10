from flask import Flask, render_template, request, jsonify
import os, json
from datetime import datetime, timedelta

app = Flask(__name__)
SCORES_FILE = os.path.join(os.path.dirname(__file__), 'scores.json')

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE) as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def top_scores(scores, key_fn, limit=10):
    eligible = [s for s in scores if key_fn(s)]
    eligible.sort(key=lambda s: s['score'], reverse=True)
    return eligible[:limit]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/score', methods=['POST'])
def submit_score():
    data = request.get_json()
    scores = load_scores()
    name = data['name'][:20]
    existing = next((s for s in scores if s['name'] == name), None)
    if existing:
        existing['score'] = data['score']
        existing['level'] = data['level']
        existing['ts'] = datetime.now().isoformat()
    else:
        scores.append({
            'name': name,
            'score': data['score'],
            'level': data['level'],
            'ts': datetime.now().isoformat()
        })
    save_scores(scores)
    return jsonify({'ok': True})

@app.route('/api/leaderboard')
def leaderboard():
    scores = load_scores()
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    all_time = top_scores(scores, lambda s: True)
    daily = top_scores(scores, lambda s: datetime.fromisoformat(s['ts']) >= today_start)
    weekly = top_scores(scores, lambda s: datetime.fromisoformat(s['ts']) >= week_start)

    return jsonify({
        'all_time': all_time,
        'daily': daily,
        'weekly': weekly
    })

@app.route('/api/check_high', methods=['POST'])
def check_high():
    data = request.get_json()
    score_val = data['score']
    scores = load_scores()
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    all_time = top_scores(scores, lambda s: True)
    daily = top_scores(scores, lambda s: datetime.fromisoformat(s['ts']) >= today_start)
    weekly = top_scores(scores, lambda s: datetime.fromisoformat(s['ts']) >= week_start)

    is_high = False
    reasons = []

    if len(all_time) < 10 or score_val >= (all_time[-1]['score'] if all_time else 0):
        is_high = True
        reasons.append('all_time')
    if len(daily) < 10 or score_val >= (daily[-1]['score'] if daily else 0):
        is_high = True
        reasons.append('daily')
    if len(weekly) < 10 or score_val >= (weekly[-1]['score'] if weekly else 0):
        is_high = True
        reasons.append('weekly')

    return jsonify({'is_high': is_high, 'reasons': reasons})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
