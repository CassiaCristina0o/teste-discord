"""Posts the pushed commit to a Discord channel through a webhook."""
import json
import os
import urllib.request

with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
    event = json.load(f)

commit = event["head_commit"]
repo = event["repository"]
title = commit["message"].splitlines()[0]

embed = {
    "title": title[:256],
    "url": commit["url"],
    "description": (
        f"**Author:** {commit['author']['name']}\n"
        f"[Repository]({repo['html_url']}) · "
        f"[See the change]({commit['url']}) · "
        f"[View the site]({os.environ['SITE_URL']})"
    ),
}

request = urllib.request.Request(
    os.environ["DISCORD_WEBHOOK"],
    data=json.dumps({"embeds": [embed]}).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "teste-discord-actions"},
)
with urllib.request.urlopen(request) as response:
    print("Discord answered", response.status)
