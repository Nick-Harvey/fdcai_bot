import os
import threading
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from Google_Sheets.google_sheets_client import GoogleSheetsClient
from Announcements.announcement_manager import AnnouncementManager
from Showrunner.slack_notifier import SlackNotifier

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Google Sheets API scope and sample spreadsheet details
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
run_of_show_sheet = "13nL6LpZZWeYIChRyngRX60DAKGQhP1T-jStotRiKHPs"
run_of_show_range = "devAnnouncements"

# Initialize Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def run_socket_mode_handler():
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()


def main():
    # Main function
    client = GoogleSheetsClient(SCOPES, "token.json", "credentials.json")
    notifier = SlackNotifier(os.environ.get("SLACK_BOT_TOKEN"))

    # Register the team_join event handler
    notifier.handle_team_join(app)

    # Create an instance of AnnouncementManager and start processing announcements
    announcement_manager = AnnouncementManager(client, notifier)
    announcement_manager.process_announcements(run_of_show_sheet, run_of_show_range)


if __name__ == "__main__":
    socket_mode_thread = threading.Thread(target=run_socket_mode_handler)
    socket_mode_thread.start()
    print("SocketModeHandler is running asynchronously in the background.")
    main()
