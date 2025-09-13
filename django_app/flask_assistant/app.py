from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)
DJANGO_API = "http://django:8000/api"  # service name in docker-compose

@app.route("/assistant", methods=["POST"])
def assistant():
    query = request.json.get("query", "").lower()

    # Log progress
    m = re.match(r"log\s+(\d+)\s*(min|minutes)?\s+([a-zA-Z ]+)", query)
    if m:
        minutes = int(m.group(1))
        task = m.group(3).strip().title()
        requests.post(f"{DJANGO_API}/logs/", json={
            "task": task, "minutes": minutes, "xp_gain": minutes // 5 * 10
        })
        return jsonify({"message": f"Logged {minutes} minutes to {task}"})

    # Set goal
    m = re.match(r"set\s+goal\s+([a-zA-Z ]+)\s+(\d+)", query)
    if m:
        task = m.group(1).title()
        val = int(m.group(2))
        requests.patch(f"{DJANGO_API}/tasks/{task}/", json={"goal_min": val})
        return jsonify({"message": f"Set goal for {task} to {val} minutes"})

    return jsonify({"message": "Command not recognized."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
