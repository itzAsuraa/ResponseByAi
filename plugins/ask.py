from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from pyrogram.types import Message
from info import *


# Function to query the AI API
def ask_query(query, model=None):
    default_model = 'gpt-4o'
    system_prompt = """You are a helpful assistant. Your name is Tanu, and your owner's name is Captain, known as @itzAsuraa."""

    model = model or default_model

    if model == default_model:
        query = f"{system_prompt}\n\nUser: {query}"

    encoded_query = urllib.parse.quote(query)
    url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("result", "No response found.")
    else:
        return f"Error fetching response from API. Status code: {response.status_code}"

# Function to simulate typing action
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    """Simulate typing action for a specified duration before sending a response."""
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Handler for the "/ask" command
@Client.on_message(filters.command("ask"))
async def handle_query(client, message):
    if len(message.command) < 2:
        await message.reply_text("<b>Please provide a query to ask.</b>")
        return

    user_query = message.text.split(maxsplit=1)[1]

    # Get user's mention
    user_mention = message.from_user.mention

    # Simulate typing action before sending the response
    await send_typing_action(client, message.chat.id, duration=2)

    # Fetch the response from the AI API
    response = ask_query(user_query)

    # Send the response back to the user with mention
    await message.reply_text(f"{user_mention}, <b>{response}</b>")

