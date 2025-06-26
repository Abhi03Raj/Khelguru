# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import uuid
import json
import requests
from datetime import datetime, timedelta
from joblib import load

app = Flask(__name__)
CORS(app)

DATA_FILE = 'player_data_1000.csv'
STANDARD_STATS_FILE = 'standard_stats.json'
EXPRESS_SAVE_URL = 'http://localhost:5000/save-stats'

# Load ML model for promotion prediction
promotion_model = load("promotion_predictor.pkl")

# Tier mapping for model input
tier_map = {
    "Bronze": 0, "Silver": 1, "Gold": 2,
    "Platinum": 3, "Diamond": 4, "Master": 5, "Grandmaster": 6
}

def is_promotion_ready(stats):
    features = [[
        stats.get("kdRatio", 0),
        stats.get("avgDamage", 0),
        stats.get("avgSurvivalTime", 0),
        stats.get("winRatio", 0),
        stats.get("headshotPercentage", 0),
        tier_map.get(stats.get("tier", "Bronze"), 0)
    ]]
    prediction = promotion_model.predict(features)[0]
    return bool(prediction)

def generate_drills_and_opinions(stats):
    kd = stats.get('kdRatio', 0)
    damage = stats.get('avgDamage', 0)
    survival = stats.get('avgSurvivalTime', 0)
    win_rate = stats.get('winRatio', 0)
    headshot = stats.get('headshotPercentage', 0)

    drills, tips = set(), set()

    if headshot < 10:
        drills |= {
            "1v1 M416 Headshot only (000-010-529)",
            "Aim Lab - Headshot drills"
        }
        tips |= {
            "Focus on crosshair placement around upper chest/neck",
            "Use ADS + gyroscope for sharper adjustments"
        }
    elif headshot < 20:
        tips.add("You’re improving. Focus on fast flicks in close-range battles")

    if damage < 250:
        drills |= {
            "Training Map – Mid-range recoil control with M416",
            "M4 vs UMP 2v2 (000-010-525)"
        }
        tips.add("Focus on 5-finger claw grip to handle recoil better")
    if damage > 500:
        tips.add("Excellent damage output – maintain your distance awareness")

    if survival < 6:
        drills |= {
            "Erangel Hill Survival (000-010-329)",
            "Zone survival custom rooms"
        }
        tips |= {
            "Land on edge zones to loot peacefully",
            "Avoid hot drops unless needed"
        }
    elif survival < 10:
        tips.add("Good survival instincts – work on final zone positioning")

    if win_rate < 20:
        drills.add("Sanhok Classic mode with squad coordination")
        tips.add("Play with mic to enhance real-time team coordination")

    # Always include some general drills & tips
    drills |= {
        "Gun Game – Weapon switching speed test",
        "Training Map – SMG vs AR recoil battle",
        "Cheer Park sniper duels"
    }
    tips |= {
        "Participate in weekly training challenges",
        "Master one long-range weapon and one short-range",
        "Join scrims/customs to experience competitive fights"
    }

    return {
        "drills": ", ".join(drills),
        "opinions": ", ".join(tips)
    }

@app.route('/submit-stats', methods=['POST'])
def submit_stats():
    new_data = request.json
    if not new_data:
        return jsonify({'error': 'Invalid or empty data'}), 400

    feedback = generate_drills_and_opinions(new_data)
    username = new_data.get('username', None)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check promotion status using ML model
    is_ready = is_promotion_ready(new_data)

    # Save to CSV
    row = {
        'Player_ID': str(uuid.uuid4()),
        'Player_Name': username or 'Guest',
        'K/D_Ratio': new_data['kdRatio'],
        'Avg_Damage': new_data['avgDamage'],
        'Survival_Time': new_data['avgSurvivalTime'],
        'Tier': new_data['tier'],
        'Win_Rate (%)': new_data['winRatio'],
        'Headshot_Rate (%)': new_data['headshotPercentage'],
        'Drills': feedback['drills'],
        'Opinions': feedback['opinions'],
        'Promotion_Ready': int(is_ready),
        'Date': timestamp
    }
    df = pd.DataFrame([row])
    if os.path.exists(DATA_FILE):
        old_df = pd.read_csv(DATA_FILE)
        df = pd.concat([old_df, df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    # Forward to Express for registered users
    if username:
        try:
            payload = {
                'username': username,
                'stats': {
                    'kdRatio': new_data['kdRatio'],
                    'avgDamage': new_data['avgDamage'],
                    'avgSurvivalTime': new_data['avgSurvivalTime'],
                    'winRatio': new_data['winRatio'],
                    'headshotPercentage': new_data['headshotPercentage'],
                    'tier': new_data['tier'],
                    'tips': feedback['opinions'].split(', ')[:2],
                    'drills': feedback['drills'].split(', ')[:2],
                    'timestamp': timestamp
                }
            }
            requests.post(EXPRESS_SAVE_URL, json=payload, timeout=2)
        except Exception as e:
            print(f"Error saving to Express: {e}")

    return jsonify({
        'message': 'Stats processed successfully.',
        'drills': feedback['drills'],
        'opinions': feedback['opinions'],
        'promotionReady': is_ready
    })

@app.route('/api/standards', methods=['GET'])
def get_standards():
    tier = request.args.get('tier')
    if not tier:
        return jsonify({'error': 'Tier is required'}), 400
    try:
        with open(STANDARD_STATS_FILE) as f:
            standards = json.load(f)
        return jsonify(standards.get(tier, {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weekly-goals/<username>', methods=['GET'])
def get_weekly_goal(username):
    try:
        # Get recent history from Express backend
        resp = requests.get(f"http://localhost:5000/api/user/history/{username}", timeout=3)
        history = resp.json()

        # Filter last 7 days
        cutoff = datetime.now() - timedelta(days=7)
        recent = [
            h for h in history
            if datetime.strptime(h['timestamp'], "%Y-%m-%d %H:%M:%S") >= cutoff
        ]

        if not recent:
            return jsonify({"message": "No recent data found"}), 404

        # Average stats over the last 7 days
        stat_keys = ["kdRatio", "avgDamage", "avgSurvivalTime", "winRatio", "headshotPercentage"]
        weekly_avg = {
            stat: sum(h[stat] for h in recent) / len(recent)
            for stat in stat_keys
        }

        # Get standard for current tier
        tier = recent[0]["tier"]
        with open(STANDARD_STATS_FILE) as f:
            standards = json.load(f)
        tier_std = standards.get(tier)

        if not tier_std:
            return jsonify({"error": "No standard found for tier"}), 500

        # Identify weakest stat by gap from standard
        gaps = {
            stat: weekly_avg[stat] - tier_std.get({
                "kdRatio": "K/D_Ratio",
                "avgDamage": "Avg_Damage",
                "avgSurvivalTime": "Survival_Time",
                "winRatio": "Win_Rate (%)",
                "headshotPercentage": "Headshot_Rate (%)"
            }[stat], 0)
            for stat in stat_keys
        }

        weakest_stat = min(gaps, key=gaps.get)
        goal_target = round(tier_std.get({
            "kdRatio": "K/D_Ratio",
            "avgDamage": "Avg_Damage",
            "avgSurvivalTime": "Survival_Time",
            "winRatio": "Win_Rate (%)",
            "headshotPercentage": "Headshot_Rate (%)"
        }[weakest_stat], 0) * 1.1, 1)

        # Friendly message
        stat_names = {
            "kdRatio": "K/D Ratio",
            "avgDamage": "Average Damage",
            "avgSurvivalTime": "Survival Time",
            "winRatio": "Win Rate",
            "headshotPercentage": "Headshot Percentage"
        }

        message = f"🎯 Focus on your {stat_names[weakest_stat]}! Try to reach {goal_target}+ this week."

        return jsonify({
            "stat": weakest_stat,
            "target": goal_target,
            "message": message
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
