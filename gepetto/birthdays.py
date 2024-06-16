import os
from datetime import datetime

def get_today_formatted():
    today = datetime.now()
    day = today.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    month_name = today.strftime("%B")
    return f"the {day}{suffix} of {month_name}"

async def get_birthday_message(bot, chatbot):
    birthdays = os.getenv('DISCORD_BOT_BIRTHDAYS', "").split(",")
    # each birthday will be formatted as "discord_username:dd/mm"
    if len(birthdays) == 0:
        return
    today_string = datetime.now().strftime("%d/%m")
    date_string = get_today_formatted()
    for birthday in birthdays:
        if today_string in birthday:
            channel = bot.get_channel(int(os.getenv('DISCORD_BOT_CHANNEL_ID', 'Invalid').strip()))
            birthday_user_id = birthday.split(":")[0]
            user = await bot.fetch_user(birthday_user_id)
            if user is None:
                return
            messages = [
                {
                    'role': 'system',
                    'content': "You are a helpful AI assistant who specialises in finding unusual, esoteric and obscure facts about specific dates in the style of newspapr 'On this day in 1905 ...'.  You should ONLY respond with the fact, no other text."
                },
                {
                    'role': 'user',
                    'content': f'Can you tell me something interesting and unusual that happened on this day in history on {date_string}?'
                },
            ]

            response = await chatbot.chat(
                messages=messages,
                temperature=1.0,
            )

            message = response.message[:1900]
            message = message.replace("Sure! ", '')
            message = message.replace("Here's a random fact for you: ", '')
            message = message.replace("Certainly! ", '')
            await channel.send(f"Happy birthday {user.mention}! {message}")
