from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

dev_channel = "C055L0EE2QN"


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

    def send_welcome_message(self, user_id):
        welcome_message = "Welcome to the server! Let us know if you have any questions."

        welcome_messsage_block = [
            {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":coral:  Welcome to the Future of Data Centric AI Slack Server  :coral:",
                        },
                    },
                    {"type": "context", "elements": [{"text": "*FDCAI Jun 7-8th*  |  future.snorkel.ai", "type": "mrkdwn"}]},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Please take a minute to review Snorkels Code of Conduct* \n Everyone is welcome, but please abide by our code-of-conduct to ensure a respectful and inclusive environment for all.",
                        },
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Code of conduct", "emoji": True},
                            "url": "https://snorkel.ai/#",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": " :compass: | *Here's a few things to help get you started* | :compass:",
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "1. *Download the Agenda* "},
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Get the agenda", "emoji": True},
                            "style": "primary",
                            "url": "#",
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "2. *Vote for your favorite research poster*"},
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Take me to those posters!", "emoji": True},
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "3. * For assistance, mention `@mods` in any channel and someone from the Snorkel will reach out. There is also <C057R9U8EF6|#fdcai-assistance> if you want to the mod team 1:1.*",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": ":calendar: |   *Upcoming Events*  | :calendar: "},
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*May 22nd* - :diving_mask: Snorkel Founders AMA 12:00pm EST"},
                        "accessory": {"type": "button", "text": {"type": "plain_text", "text": "Join #AMA", "emoji": True}},
                    },
                    {"type": "section", "text": {"type": "mrkdwn", "text": "*June 7* - Future of Data Centric AI Day 1"}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": "*June 8* - Future of Data Centric AI Day 2"}},
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*June 21st* - Ai Leaders Forum - NYC, in-person"},
                        "accessory": {"type": "button", "text": {"type": "plain_text", "text": "RSVP", "emoji": True}},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": ":speech_balloon: | *Connect with others* | :speech_balloon:"},
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Dive into our vibrant community and ink-credible conversations by joining our topic-focused channels. Search for channels in slack that start with `discussion-`: \n \n *Examples*: \n `discussion-nlp` \n `discussion-llms` \n `discussion-weak-supervision`\n ",
                            "verbatim": False,
                        },
                    },
                    {"type": "divider"},
                    {"type": "divider"},
                    {
                        "type": "context",
                        "elements": [
                            {"type": "mrkdwn", "text": ":pushpin: Pssst... We're hiring! Check out our *open roles*."}
                        ],
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Click Me", "emoji": True},
                                "value": "click_me_123",
                                "action_id": "actionId-0",
                            }
                        ],
                    },
                ]
            }
        ]

        try:
            response = self.client.conversations_open(users=user_id)
            channel_id = response["channel"]["id"]
            self.client.chat_postMessage(channel=channel_id, text=welcome_message, blocks=welcome_messsage_block)
        except SlackApiError as e:
            print(f"Error sending welcome message: {e}")

    def handle_team_join(self, app):
        @app.event("team_join")
        def _handle_team_join(body, logger):
            user_id = body["event"]["user"]["id"]
            self.send_welcome_message(user_id)
