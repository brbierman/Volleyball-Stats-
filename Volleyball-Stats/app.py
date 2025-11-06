from flask import Flask, jsonify

import requests

from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/stats/<int:event_id>")

def get_stats(event_id):

    url = f"https://stats.statbroadcast.com/videoboard/?id={event_id}"

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Page title

        title = soup.title.string if soup.title else "Unknown Event"

        # Team names

        teams = [t.get_text(strip=True) for t in soup.select(".teamname")]

        # Scores

        scores = [s.get_text(strip=True) for s in soup.select(".score")]

        # Extract player stats tables (if available)

        player_stats = []

        tables = soup.find_all("table")

        for table in tables:

            headers = [th.get_text(strip=True) for th in table.find_all("th")]

            if not headers:

                continue  # skip non-data tables

            rows = []

            for row in table.find_all("tr")[1:]:

                cols = [td.get_text(strip=True) for td in row.find_all("td")]

                if cols:

                    rows.append(dict(zip(headers, cols)))

            if rows:

                player_stats.append({

                    "headers": headers,

                    "players": rows

                })

        data = {

            "event_id": event_id,

            "source": "StatBroadcast",

            "url": url,

            "title": title,

            "teams": teams,

            "scores": scores,

            "player_stats": player_stats

        }

        return jsonify(data)

    except Exception as e:

        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
StatMonitr Stat Feed
 