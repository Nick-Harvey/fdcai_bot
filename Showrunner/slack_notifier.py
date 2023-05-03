from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


dev_channel = "C055L0EE2QN"

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


class SlackNotifier:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def upcoming_session(self, channel, text, speakers, session_time, stage):
        upcoming_session_block = [
            {"type": "section", "text": {"type": "plain_text", "emoji": True, "text": "Upcoming session"}},
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<https://future.snorkel.ai/| {text}>*\n{session_time}\n{stage}\n{speakers}",
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notifications.png",
                    "alt_text": "FDCAI session thumbnail",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*<https://future.snorkel.ai/agenda/| Read the full agenda>*"},
            },
        ]

        try:
            self.client.chat_postMessage(channel=channel, text=text, blocks=upcoming_session_block)

        except SlackApiError as e:
            print(f"Error sending message: {e}")

    # Listen for the team_join event
    @app.event("team_join")
    def handle_team_join(event, client, logger, welcome_message):
        user_id = event["user"]["id"]
        try:
            # Open a DM with the new user
            response = client.conversations_open(users=user_id)
            channel_id = response["channel"]["id"]

            # Send the welcome message to the new user
            client.chat_postMessage(channel=channel_id, text=welcome_message)
        except SlackApiError as e:
            logger.error(f"Error sending welcome message: {e}")
