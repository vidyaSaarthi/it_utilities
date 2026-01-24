import pandas as pd
from datetime import datetime, timedelta
import calendar
import asyncio, telegram
from telegram.constants import ParseMode

def send_telegram(grp, token_str, msg):
    try:
        telegram_msg = msg
        telegram_group_id = grp
        bot = telegram.Bot(token=token_str)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(bot.send_message(chat_id=telegram_group_id, text=telegram_msg, parse_mode='HTML'))
    except:
        pass

# --- CONFIGURATION ---
FILE_PATH = r"C:\Users\Shubham Aggarwal\Downloads\Forms Schedule.xlsx"  # Replace with your actual file name
SHEET_NAME = 'Sheet1'  # Replace with your actual sheet name


def get_month_number(month_val):
    """Helper to convert Month name (January) or abbreviation (Jan) to number."""
    if pd.isna(month_val):
        return None
    try:
        return int(float(month_val))
    except ValueError:
        try:
            return list(calendar.month_name).index(str(month_val).title())
        except ValueError:
            try:
                return list(calendar.month_abbr).index(str(month_val).title())
            except ValueError:
                return None


def preprocess_data(df):
    """
    Cleans data and creates distinct 'Start_Datetime' and 'End_Datetime' objects.
    """
    # 1. Handling Missing Start Time (Default to 12:00 AM)
    df['Start Time Hours'] = df['Start Time Hours'].fillna(12)
    df['Start Time Minutes'] = df['Start Time Minutes'].fillna(0)
    df['Start Time (AM/PM)'] = df['Start Time (AM/PM)'].fillna('AM')

    # 2. Handling Missing End Time (Default to 11:59 PM)
    df['End Time Hours'] = df['End Time Hours'].fillna(11)
    df['End Time Minutes'] = df['End Time Minutes'].fillna(59)
    df['End Time (AM/PM)'] = df['End Time (AM/PM)'].fillna('PM')

    start_datetimes = []
    end_datetimes = []

    for index, row in df.iterrows():
        # --- PROCESS START DATE ---
        try:
            # Rule: If Start Date/Month/Year is missing, it started in the past.
            if pd.isna(row['Start date']):
                s_day = 1
            else:
                s_day = int(row['Start date'])

            if pd.isna(row['Start Month']):
                s_month = 1
            else:
                s_month = get_month_number(row['Start Month'])

            if pd.isna(row['Start Year']):
                s_year = 1
            else:
                s_year = int(row['Start Year'])

            s_hour = int(row['Start Time Hours'])
            if row['Start Time (AM/PM)'].upper() == 'PM' and s_hour != 12:
                s_hour += 12
            if row['Start Time (AM/PM)'].upper() == 'AM' and s_hour == 12:
                s_hour = 0

            s_dt = datetime(s_year, s_month, s_day, s_hour, int(row['Start Time Minutes']))
        except Exception as e:
            print(f"Error parsing Start Date for row {index}: {e}")
            s_dt = None

        start_datetimes.append(s_dt)

        # --- PROCESS END DATE ---
        try:
            e_year = int(row['End Year'])
            e_month = get_month_number(row['End Month'])

            if pd.isna(row['End Date']):
                # End of specific month logic
                last_day = calendar.monthrange(e_year, e_month)[1]
                e_day = last_day
                e_hour, e_minute = 23, 59
            else:
                e_day = int(row['End Date'])
                e_hour = int(row['End Time Hours'])
                e_minute = int(row['End Time Minutes'])

                if row['End Time (AM/PM)'].upper() == 'PM' and e_hour != 12:
                    e_hour += 12
                if row['End Time (AM/PM)'].upper() == 'AM' and e_hour == 12:
                    e_hour = 0

            e_dt = datetime(e_year, e_month, e_day, e_hour, e_minute)

        except Exception as e:
            print(f"Error parsing End Date for row {index}: {e}")
            e_dt = None

        end_datetimes.append(e_dt)

    df['Start_Datetime'] = start_datetimes
    df['End_Datetime'] = end_datetimes
    df = df.dropna(subset=['Start_Datetime', 'End_Datetime'])
    return df


def generate_alerts(df):
    now = datetime.now()
    date_fmt = '%d-%b-%Y %H:%M:%S'

    # Dictionaries to hold lists of tuples: (Date_Object, Message_String)
    daily_live_alerts = {}
    ending_soon_alerts = {}
    starting_soon_alerts = {}

    print(f"--- Generating Alerts for {now.strftime(date_fmt)} ---\n")

    for index, row in df.iterrows():
        stream = row['Stream']
        activity = row['Form Activities']
        start_dt = row['Start_Datetime']
        end_dt = row['End_Datetime']

        start_str = start_dt.strftime(date_fmt)
        end_str = end_dt.strftime(date_fmt)

        # --- ALERT 1: Daily Morning Alerts (Open and Live) ---
        if start_dt <= now <= end_dt:
            if stream not in daily_live_alerts: daily_live_alerts[stream] = []

            note = ""
            if pd.isna(row['End Date']):
                note = " (Open all month)"

            msg = f"{activity}{note} \n         <b>Ends:</b> {end_str}\n"
            # Store tuple: (Sort_Key, Message) -> Sort by End Date
            daily_live_alerts[stream].append((end_dt, msg))

        # --- ALERT 2: Special Deadline Alerts ---
        time_remaining = end_dt - now
        deadline_msg = None

        if timedelta(hours=0) < time_remaining <= timedelta(hours=24):
            deadline_msg = "Ends in < 24 Hours"
        elif timedelta(days=2) < time_remaining <= timedelta(days=3):
            deadline_msg = "Ends in 3 Days"
        elif timedelta(days=6) < time_remaining <= timedelta(days=7):
            deadline_msg = "Ends in 1 Week"

        if deadline_msg:
            if stream not in ending_soon_alerts: ending_soon_alerts[stream] = []
            msg = f"{activity} - {deadline_msg} ({end_str})"
            # Store tuple: (Sort_Key, Message) -> Sort by End Date
            ending_soon_alerts[stream].append((end_dt, msg))

        # --- ALERT 3: Starting Soon ---
        time_until_start = start_dt - now
        if timedelta(hours=0) < time_until_start <= timedelta(hours=24):
            if stream not in starting_soon_alerts: starting_soon_alerts[stream] = []
            msg = f"{activity} starts at {start_str}"
            # Store tuple: (Sort_Key, Message) -> Sort by START Date
            starting_soon_alerts[stream].append((start_dt, msg))

    # --- HELPER TO PRINT SORTED LISTS ---
    def print_category(title, alert_dict):
        print("==========================================")
        print(title)
        print("==========================================")

        telegram_msg= "==========================================\n"
        telegram_msg = telegram_msg + title
        telegram_msg = telegram_msg + "\n=========================================="
        # print(title)
        # print("==========================================")

        if not alert_dict:
            print("No alerts found.")
            telegram_msg = telegram_msg + "\nNo alerts found.\n"
            send_telegram('@VS_Notices', '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14', telegram_msg)
            return

        # Sort Streams Alphabetically first
        for stream in sorted(alert_dict.keys()):
            print(f"\n>> <b>👉️ Stream: {stream}\n</b>")
            telegram_msg = telegram_msg + f"\n<b>👉 Stream: {stream}</b>\n\n"


            # Retrieve the list of tuples for this stream
            activities = alert_dict[stream]

            # SORT HERE: Sort based on the first item in the tuple (the date object)
            activities.sort(key=lambda x: x[0])

            # Print only the message (second item in tuple)
            for _, message in activities:
                print(f"   🔹 <b>{message}</b>")
                telegram_msg = telegram_msg + f"   🔹 {message}\n"
        print("\n")
        telegram_msg = telegram_msg + "\n"
        send_telegram('@VS_Notices', '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14', telegram_msg)

    # --- PRINTING THE REPORT ---

    print_category("<b>🟢 DAILY LIVE FORM ACTIVITIES (OPEN NOW)</b>", daily_live_alerts)

    print_category("<b>🟢 DEADLINE ALERTS (Ends in 1 Week, 3 Days, or 24 Hrs)</b>",
                   ending_soon_alerts)
    print_category("<b>🟢 UPCOMING STARTS (Next 24 Hrs)</b>", starting_soon_alerts)


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
        df_clean = preprocess_data(df)
        generate_alerts(df_clean)
    except FileNotFoundError:
        print(f"Error: The file '{FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")