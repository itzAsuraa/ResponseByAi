from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import requests
import asyncio
from info import *  # Assuming sensitive info like API keys and configurations are imported here
from database import *  # Assuming database functions (like FSUB, get_fsub) are defined here

BASE_URL = "https://chatwithai.codesearch.workers.dev/?chat="

def ask_query(query: str) -> str:
    try:
        # Send GET request to the API
        response = requests.get(f"{BASE_URL}{query}")
        response.raise_for_status()
        # Parse JSON response
        data = response.json()  # Convert the response to a JSON object
        # Extract and return the "data" field if present
        return data.get("data", "⚠️ Error: Unexpected response format")
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error: {str(e)}"
    except json.JSONDecodeError:
        return "⚠️ Error: Failed to decode the response from the server."

async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(duration)

@Client.on_message(filters.command("ask"))
async def ask_query_command(client: Client, message: Message):
    if FSUB and not await get_fsub(client, message):
        return
    query = message.text.split(" ", 1)
    if len(query) > 1:
        await send_typing_action(client, message.chat.id)
        reply = ask_query(query[1])
        await message.reply_text(f"{message.from_user.mention}, {reply} 🚀")
    else:
        await message.reply_text("📝 Please provide a query to ask GPT-4. Don't be shy, let's chat! 🤖💬.")

@Client.on_message(filters.mentioned & filters.group)
async def handle_mention(client: Client, message: Message):
    if FSUB and not await get_fsub(client, message):
        return
    user_text = (
        message.reply_to_message.text.strip()
        if message.reply_to_message
        else message.text.split(" ", 1)[1].strip()
        if len(message.text.split(" ", 1)) > 1
        else ""
    )
    if user_text:
        await send_typing_action(client, message.chat.id)
        reply = ask_query(user_text)
        await message.reply_text(f"{message.from_user.mention}, {reply} 🚀")
    else:
        await message.reply("👋 Please ask a question after mentioning me! I’m here to help! 😊")