from bs4 import BeautifulSoup, NavigableString
import html
import requests
import json

def process_tag(tag):
    slack_markup = ""
    if isinstance(tag, NavigableString):
        return tag
    if tag.name == 'strong':
        slack_markup += f"*{tag.get_text()}*"
    elif tag.name == 'a':
        slack_markup += f"<{tag['href']}|{tag.get_text()}>"
    elif tag.name == 'p':
        for child in tag.children:
            slack_markup += process_tag(child)
        slack_markup += "\n"
    elif tag.name == 'hr':
        slack_markup += "------------------------------\n"
    elif tag.name == 'h3':
        slack_markup += f"*{tag.get_text()}*\n"
    return slack_markup

def html_to_slack_markup(html_content):
    slack_markup = ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup:
        slack_markup += process_tag(tag)
    slack_markup = html.unescape(slack_markup)
    return slack_markup

def post_to_slack(webhook_url, message, username=None, icon_emoji=None, icon_url=None):
    payload = {
        "text": message,
        "mrkdwn": True  # Enable Slack markup
    }
    
    if username:
        payload["username"] = username
    
    if icon_emoji:
        payload["icon_emoji"] = icon_emoji
    
    if icon_url:
        payload["icon_url"] = icon_url
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        print("Successfully posted message to Slack.")
    else:
        print(f"Failed to post message to Slack. Status code: {response.status_code}, Reason: {response.text}")
