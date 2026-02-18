import pandas as pd
from datetime import datetime, timedelta
import calendar
import asyncio, telegram
import matplotlib.pyplot as plt
import requests

def send_telegram(grp, token_str, msg):
    try:
        telegram_msg = msg
        telegram_group_id = grp
        bot = telegram.Bot(token=token_str)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(bot.send_message(chat_id=telegram_group_id, text=telegram_msg, parse_mode='HTML'))
    except Exception as e:
        print(e)

def send_telegram_photo(file_path, caption, BOT_TOKEN, grp):
    """Sends an image file to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(file_path, 'rb') as photo:
            payload = {'chat_id': grp, 'caption': caption}
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            if response.status_code != 200:
                print(f"Failed to send photo: {response.text}")
    except Exception as e:
        print(f"Error sending photo: {e}")

# --- CONFIGURATION ---
FILE_PATH = r"Forms Schedule.xlsx"  # Replace with your actual file name
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
    all_activities_schedule = {}

    print(f"--- Generating Alerts for {now.strftime(date_fmt)} ---\n")

    for index, row in df.iterrows():
        stream = row['Stream']
        form_name = row['Form Name']
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

            msg = f"{form_name} - {activity}{note} \n         <b>Ends:</b> {end_str}\n"
            # Store tuple: (Sort_Key, Message) -> Sort by End Date
            daily_live_alerts[stream].append((end_dt, msg))

        # --- ALERT 2: Special Deadline Alerts ---
        time_remaining = end_dt - now
        deadline_msg = None

        if timedelta(hours=0) < time_remaining <= timedelta(hours=24):
            deadline_msg = "Ends in &lt; 24 Hours"
        elif timedelta(days=2) < time_remaining <= timedelta(days=3):
            deadline_msg = "Ends in 3 Days"
        elif timedelta(days=6) < time_remaining <= timedelta(days=7):
            deadline_msg = "Ends in 1 Week"

        if deadline_msg:
            if stream not in ending_soon_alerts: ending_soon_alerts[stream] = []
            msg = f"{form_name} - {activity} - {deadline_msg} ({end_str})"
            # Store tuple: (Sort_Key, Message) -> Sort by End Date
            ending_soon_alerts[stream].append((end_dt, msg))

        # --- ALERT 3: Starting Soon ---
        time_until_start = start_dt - now
        if timedelta(hours=0) < time_until_start <= timedelta(hours=24):
            if stream not in starting_soon_alerts: starting_soon_alerts[stream] = []
            msg = f"{form_name} - {activity} starts at {start_str}"
            # Store tuple: (Sort_Key, Message) -> Sort by START Date
            starting_soon_alerts[stream].append((start_dt, msg))

        # --- ALERT 4: All form shedules
        if stream not in all_activities_schedule:
            all_activities_schedule[stream] = {}

        if form_name not in all_activities_schedule[stream]:
            all_activities_schedule[stream][form_name] = []

            # Store tuple: (Start Date Object, Activity Name, Start String, End String)
        all_activities_schedule[stream][form_name].append((start_dt, activity, start_str, end_str))
        # print(all_activities_schedule)

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

    def send_full_schedule_report_prev(title, data_dict):

        msg= "==========================================\n"
        msg = msg + title
        msg = msg + "\n=========================================="

        if not data_dict: return
        emoji = ''
        # This message can get long, so we might want to start fresh
        # msg = msg + f"<b>{emoji} {title}</b>\n"

        # 1. Sort Streams Alphabetically
        for stream in sorted(data_dict.keys()):
            msg = f"\n<b>Stream: {stream}</b>\n"

            # 2. Sort Form Names Alphabetically
            forms = data_dict[stream]
            for form_name in sorted(forms.keys()):
                msg += f"\n🔹<b>{form_name}</b>\n"

                # 3. Sort Activities by Start Date (Ascending)
                activities = forms[form_name]
                activities.sort(key=lambda x: x[0])

                for start_dt, act_name, s_str, e_str in activities:
                    # Determine status icon
                    icon = "🔘"
                    if start_dt > now:
                        icon = "🔜"  # Future
                    elif start_dt <= now and (start_dt + timedelta(days=365 * 10)) > now:
                        icon = "🟢"  # Active (approx logic)

                    msg += f"   👉 <b>Activity -</b>{act_name}\n          <b>Start:</b> {s_str}\n          <b>End:</b>   {e_str}\n\n"

        # send_telegram_message(msg)
            print(msg)
            send_telegram('@VS_Notices', '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14', msg)
        # print(f"Sent: {title}")

    def send_full_schedule_report(title, data_dict):

        emoji=''
        if not data_dict: return

        print("Generating Stream-wise Schedule Images...")

        # --- CONFIGURATION: EDIT YOUR CONTACT INFO HERE ---
        WATERMARK_TXT = "VidyaSaarthi"
        WATERMARK_CONTACT = "    Contact: +91-8600164008, +91 90343 75324"

        # NEW: Fix the gap to exactly 1.0 inch regardless of image height
        FIXED_GAP_INCHES = 1.0

        # Loop through each stream separately
        for stream in sorted(data_dict.keys()):
            print(f"  > Processing Stream: {stream}")

            table_data = []
            # We removed 'Stream' column since the file is specific to one stream
            columns = ["Form Name", "Activity", "Start Date", "End Date"]

            forms = data_dict[stream]
            for form_name in sorted(forms.keys()):
                activities = forms[form_name]
                activities.sort(key=lambda x: x[0])

                for start_dt, act_name, s_str, e_str in activities:
                    s_date_only = s_str[:11]
                    e_date_only = e_str[:11]
                    table_data.append([form_name, act_name, s_date_only, e_date_only])

            if not table_data:
                continue

            # --- Create DataFrame for this specific stream ---
            df_table = pd.DataFrame(table_data, columns=columns)

            # --- Plotting ---
            num_rows = len(df_table)
            img_height = max(4, num_rows * 0.4 + 1.5)

            fig, ax = plt.subplots(figsize=(12, img_height))
            ax.axis('off')

            # Note: colWidths adjusted since we have 4 columns now instead of 5
            tbl = ax.table(cellText=df_table.values,
                           colLabels=df_table.columns,
                           loc='center',
                           cellLoc='left',
                           colWidths=[0.30, 0.40, 0.15, 0.15])

            # --- Styling ---
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(11)
            tbl.scale(1.1, 2)

            for (row, col), cell in tbl.get_celld().items():
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor('#40466e')
                else:
                    if row % 2 == 0: cell.set_facecolor('#f5f5f5')
                    # Now Column 0 is Form Name, so bold that
                    if col == 0: cell.set_text_props(weight='bold')

            # Dynamic Title based on Stream Name
            current_date = datetime.now().strftime('%d-%b-%Y')
            plt.title(f"{emoji} {stream} Forms Schedule (As of {current_date})",
                      fontsize=16, weight='bold', pad=30, y=1.02)

            # ==========================================
            #  CONSISTENT WATERMARK LOGIC
            # ==========================================
            # 1. Main Text (Always exact center)
            main_y = 0.5

            # 2. Contact Detail (Calculated fixed offset)
            # We convert the desired inch gap into a relative figure coordinate
            gap_adjustment = FIXED_GAP_INCHES / img_height
            contact_y = main_y - gap_adjustment

            fig.text(0.5, main_y, WATERMARK_TXT,
                     fontsize=80, color='red',
                     ha='center', va='center',
                     alpha=0.10,
                     rotation=30, weight='bold')

            fig.text(0.5, contact_y, WATERMARK_CONTACT,
                     fontsize=20, color='red',
                     ha='center', va='center',
                     alpha=0.30, rotation=30)
            # ==========================================

            # --- Save & Send Unique File ---
            # Sanitize filename (remove spaces or special chars)
            safe_stream_name = "".join([c for c in stream if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
            image_filename = f"Schedule_{safe_stream_name}.jpg"

            plt.savefig(image_filename, bbox_inches='tight', dpi=150)
            plt.close()

            print(f"    Saved: {image_filename}")
            send_telegram_photo(image_filename, f"{emoji} {stream} Forms Schedule", '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14','@VS_Notices')    # --- PRINTING THE REPORT ---

    print_category("<b>🟢 DAILY LIVE FORM ACTIVITIES (OPEN NOW)</b>", daily_live_alerts)

    print_category("<b>🟢 DEADLINE ALERTS (Ends in 1 Week, 3 Days, or 24 Hrs)</b>",
                   ending_soon_alerts)
    print_category("<b>🟢 UPCOMING STARTS (Next 24 Hrs)</b>", starting_soon_alerts)

    # send_full_schedule_report("<b>🟢 ALL FORM SCHEDULES</b>", all_activities_schedule)
    send_full_schedule_report("ALL FORM SCHEDULES", all_activities_schedule)


# def send_telegram_photo(file_path, caption):
#     """Sends an image file to Telegram."""
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
#     try:
#         with open(file_path, 'rb') as photo:
#             payload = {'chat_id': CHAT_ID, 'caption': caption}
#             files = {'photo': photo}
#             response = requests.post(url, data=payload, files=files)
#             if response.status_code != 200:
#                 print(f"Failed to send photo: {response.text}")
#     except Exception as e:
#         print(f"Error sending photo: {e}")


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