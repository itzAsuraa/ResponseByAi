from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from info import *

# Function to query the AI API
def ask_query(query, model='llama'):
    try:
        # Encode the user query for safe URL handling
        encoded_query = urllib.parse.quote(query)
        url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

        # Make the API request
        response = requests.get(url)
        if response.status_code == 200:
            # Return the result or a fallback message if no response is found
            return response.json().get("result", "🤔 I couldn't find an answer to that.")
        else:
            return f"⚠️ API Error: Unable to retrieve data. (Status code: {response.status_code})"
    except Exception as e:
        return f"⚠️ An error occurred: {e}"

# Function to simulate typing action for an engaging user experience
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Handler for the "/llama" command
@Client.on_message(filters.command("llama"))
async def handle_query(client, message):
    # Ensure a query is provided by the user
    if len(message.command) < 2:
        await message.reply_text("💬 <b>Please provide a query to ask.</b>")
        return

    # Extract the user's query and mention
    user_query = message.text.split(maxsplit=1)[1]
    user_mention = message.from_user.mention

    # Simulate typing action before sending the response
    await send_typing_action(client, message.chat.id, duration=2)

    # Get the AI response for the user query
    response = ask_query(user_query)

    # Reply with the formatted response including user mention
    await message.reply_text(
        f"{user_mention},<b>{response}</b>"
    )