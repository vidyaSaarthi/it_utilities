import pandas as pd
from datetime import datetime, timedelta
import asyncio,os, telegram
from telegram.constants import ParseMode

def send_telegram(grp, token_str, msg):
    try:
        telegram_msg = msg
        telegram_group_id = grp
        bot = telegram.Bot(token=token_str)
        asyncio.run(bot.send_message(chat_id=telegram_group_id, text=telegram_msg, parse_mode=ParseMode.MARKDOWN))
    except:
        pass

# Load your file
file_path = r'C:\Users\Shubham Aggarwal\Downloads\UG Counselling Schedule.xlsx'
df = pd.read_excel(file_path)

# --- 1. FORMAT VALIDATION ---
date_pattern = r'^\d{2}-\d{2}-\d{4}$'
# Regex for 12-hour format (e.g., 2:00 pm, 11:00 AM)
time_pattern_12h = r'^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$'
time_pattern_24h = r'^([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$'


def check_format(series, pattern):
    valid_items = series.dropna().astype(str)
    if len(valid_items) == 0: return True
    return valid_items.str.match(pattern).all()


print(f"Format Check - Date (DD-MM-YYYY): {'Passed' if check_format(df['Start Date'], date_pattern) else 'Failed'}")
print(
    f"Format Check - Time : {'Passed' if check_format(df['Start Time'], time_pattern_24h) else 'Failed (Using flexible parser)'}")

# --- 2. DATA PREPARATION ---
# Fill Missing Times with defaults
df['Start Time'] = df['Start Time'].fillna('00:00')
df['End Time'] = df['End Time'].fillna('11:59 PM')


def parse_datetime(date_str, time_str, is_end=False):
    if pd.isna(date_str):
        # If Start Date is missing but End Date exists, we treat it as having no defined start (effectively ongoing until end)
        return pd.Timestamp.min if not is_end else pd.NaT

    try:
        dt_date = datetime.strptime(str(date_str).strip(), '%d-%m-%Y')
    except ValueError:
        return pd.NaT

    # Flexible Time Parsing (Try 12-hour, then 24-hour)
    time_str = str(time_str).strip()
    dt_time = None
    for fmt in ['%I:%M %p', '%I:%M%p', '%H:%M:%S', '%H:%M']:
        try:
            dt_time = datetime.strptime(time_str, fmt).time()
            break
        except ValueError:
            continue

    # Fallback if time parsing fails completely
    if dt_time is None:
        dt_time = datetime.strptime('23:59' if is_end else '00:00', '%H:%M').time()

    return datetime.combine(dt_date, dt_time)


df['Start_Datetime'] = df.apply(lambda x: parse_datetime(x['Start Date'], x['Start Time']), axis=1)
df['End_Datetime'] = df.apply(lambda x: parse_datetime(x['End Date'], x['End Time'], is_end=True), axis=1)

# --- 3. GENERATE ALERTS ---
now = datetime.now()
today_date = now.date()
message = ''

print(f"\nReport Generated: {now.strftime('%d-%m-%Y %I:%M %p')}\n")

# ALERT 1: Activities Starting Today

starting_today = df[(df['Start_Datetime'].dt.date == now.date())]
# print("🔔 *ACTIVITIES Starting Today*")
message = message + "🔔 *ACTIVITIES Starting Today*\n\n"

if starting_today.empty:
    # print("*No activities starting Today.*")
    message = message + "*No activities starting Today.*"
else:
    for _, row in starting_today.iterrows():
        # print(row)
        start_str = row['Start_Datetime'].strftime('%I:%M %p')
        if start_str == '12:00 AM':
            start_str = ''
        else:
            start_str = '*At* ' + start_str

        # print(f"- *State - {row['State']} - {row['Round']} Round*\n- *Activity* - {row['Activity']}\n- *Starts On*: {row['Start Date']} {start_str}\n")
        message = message + f"- *State - {row['State']} - {row['Round']} Round*\n- *Activity* - {row['Activity']}\n- *Starts On*: {row['Start Date']} {start_str}\n"


# ALERT 2: Activities Ending Within 24 Hours
limit_24h = now + timedelta(hours=24)
ending_today = df[(df['End_Datetime'] <= limit_24h) & (df['End_Datetime'] > now)]
# print("\n\n🔔 *ACTIVITIES ENDING in 24 Hours*")
message = message + "\n\n🔔 *ACTIVITIES ENDING in 24 Hours*\n\n"

if ending_today.empty:

    # print("*No activities ending in next 24 hours.*")
    message = message + "*No activities ending in next 24 hours.*"
else:
    for _, row in ending_today.iterrows():
        # print(row)
        end_str = row['End_Datetime'].strftime('%I:%M %p')
        # print(f"- *State - {row['State']} - {row['Round']} Round*\n- *Activity* - {row['Activity']}\n- *Ends At*: {row['End Date']} {end_str}\n")
        message = message + f"- *State - {row['State']} - {row['Round']} Round*\n- *Activity* - {row['Activity']}\n- *Ends At*: {row['End Date']} {end_str}\n"


# ALERT 3: State Wise Ongoing/Future
# print("\n\n📅 *STATE-WISE ACTIVITY STATUS*")
message = message + "\n\n\n📅 *STATE-WISE ACTIVITY STATUS*\n"
# Filter: End Date must be in the future (or present)
active_df = df[df['End_Datetime'] >= now].copy()
active_df['Status'] = active_df['Start_Datetime'].apply(lambda x: 'Future' if x > now else 'Ongoing')

for state, group in active_df.groupby('State'):
    # print(f"\n*State: {state}*")
    message = message + f"\n*State: {state}*\n"
    group = group.sort_values('Start_Datetime')
    for _, row in group.iterrows():
        start_disp = row['Start_Datetime'].strftime('%d-%m-%Y %I:%M %p') if row[
                                                                                'Start_Datetime'] != pd.Timestamp.min else "Not Specified"
        start_disp = start_disp.replace(" 12:00 AM",'')
        end_disp = row['End_Datetime'].strftime('%d-%m-%Y %I:%M %p')
        # print(f"- [*{row['Status']}*] {row['Activity']}\n- *From*: {start_disp}  *To*: {end_disp}\n")
        message = message + f"- \[*{row['Status']}*] {row['Activity']}\n- *From*: {start_disp}  *To*: {end_disp}\n\n"


print(message)

send_telegram('@VS_Notices', '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14', message)