import asyncio
from pyrogram import Client, filters
from database import total_users

@Client.on_message(filters.private & filters.command("stats"))
async def users(bot, update):
    users = await total_users()  # Get total users from the database
    text = "Bot Status\n"
    text += f"\nTotal Users: {users}"  # Format the response message
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True  # Disable web page preview in the reply
    )