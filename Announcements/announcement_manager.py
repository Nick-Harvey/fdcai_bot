from Google_Sheets.google_sheets_client import GoogleSheetsClient
from Showrunner.slack_notifier import SlackNotifier
import logging
import time


class AnnouncementManager:
    def __init__(self, google_sheets_client, slack_notifier):
        self.google_sheets_client = google_sheets_client
        self.slack_notifier = slack_notifier

    def get_column_letter(self, column_number):
        result = []
        while column_number > 0:
            column_number, remainder = divmod(column_number - 1, 26)
            result[:0] = chr(65 + remainder)
        return "".join(result)

    def process_announcements(self, run_of_show_sheet, run_of_show_range):
        while True:
            logging.debug(f"Checking spreadsheet for new announcements...")
            run_of_show_data = self.google_sheets_client.get_sheet_data(run_of_show_sheet, run_of_show_range)
            logging.debug(f"run_of_show_data sample: {run_of_show_data}")
            if run_of_show_data:
                headers, values = run_of_show_data
                for index, row_values in enumerate(values):
                    row = dict(zip(headers, row_values))
                    if row["Priority"] == "1" and row["Approved"] == "Yes" and row["Sent"] == "0":
                        logging.debug(f"Sending message: {row['Message']}")
                        self.slack_notifier.upcoming_session(
                            row["Channel"], row["Message"], row["Speakers"], row["Datetime_to_be_sent"], row["Stage"]
                        )
                        sent_column_index = headers.index("Sent") + 1
                        cell_range = (
                            f"{run_of_show_range.split('!')[0]}!{self.get_column_letter(sent_column_index)}{index + 2}"
                        )
                        self.google_sheets_client.update_cell_value(run_of_show_sheet, cell_range, "1")
                    else:
                        logging.debug(f"Skipping message: {row['Message']}")
            else:
                logging.warning("No data found in the run_of_show_data.")
            time.sleep(10)
