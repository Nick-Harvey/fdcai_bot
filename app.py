import os
import threading
import logging
import pandas as pd
import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from listeners import register_listeners
from dotenv import load_dotenv
from Google_Sheets.google_sheets_client import GoogleSheetsClient
from Showrunner.slack_notifier import SlackNotifier

# Load environment variables
load_dotenv()

# establish current datetime
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create the log filename with the current date and time
log_filename = f"dr_bubbles_logs_{current_datetime}.log"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Set the log message format
    handlers=[
        logging.FileHandler(log_filename),  # Log to the specified file
        logging.StreamHandler(),  # Optionally, also log to the console (standard output)
    ],
)

# Google Sheets API scope and sample spreadsheet details
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
run_of_show_sheet = "13nL6LpZZWeYIChRyngRX60DAKGQhP1T-jStotRiKHPs"
run_of_show_range = "devAnnouncements"

# Initialize Slack app and logging
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# logging.basicConfig(level=logging.DEBUG)
register_listeners(app)


def run_socket_mode_handler():
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()


def main():
    # Main function
    client = GoogleSheetsClient(SCOPES, "token.json", "credentials.json")

    # Run of Show
    run_of_show_data = client.get_sheet_data(run_of_show_sheet, run_of_show_range)
    if run_of_show_data:
        df = client.gsheet_to_dataframe(run_of_show_data)
        print(df)

        notifier = SlackNotifier(os.environ.get("SLACK_BOT_TOKEN"))

        for _, row in df.iterrows():
            if row["Priority"] == "1" and row["approved"] == "Yes":
                notifier.upcoming_session("#mainstage", row["Message"])

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

    # # Run of Show
    # welcome_message = client.get_sheet_data(welcome_message, welcome_message_range)
    # if run_of_show_data:
    #     df = client.gsheet_to_dataframe(run_of_show_data)
    #     print(df)

    #     notifier = SlackNotifier(os.environ.get("SLACK_BOT_TOKEN"))

    #     for _, row in df.iterrows():
    #         if row["Priority"] == "1":
    #             notifier.upcoming_session("#mainstage", row["Message"])


if __name__ == "__main__":
    socket_mode_thread = threading.Thread(target=run_socket_mode_handler)
    socket_mode_thread.start()
    print("SocketModeHandler is running asynchronously in the background.")
    main()
