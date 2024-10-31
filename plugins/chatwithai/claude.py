from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from info import *

# Function to query the AI API
def ask_query(query, model='claude-sonnet-3.5'):
    try:
        # Encode the query for URL safety
        encoded_query = urllib.parse.quote(query)
        url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

        # Send request to the API
        response = requests.get(url)
        if response.status_code == 200:
            # Return the API result if available, otherwise a fallback message
            return response.json().get("result", "🤔 I'm not sure how to respond to that.")
        else:
            return f"⚠️ Error: Unable to fetch a response from the API. (Status code: {response.status_code})"
    except Exception as e:
        return f"⚠️ An unexpected error occurred - {e}"

# Function to simulate typing action for user interaction
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Handler for the "/claude" command
@Client.on_message(filters.command("claude"))
async def handle_query(client, message):
    # Check if the user provided a query
    if len(message.command) < 2:
        await message.reply_text("💬 <b>Please enter a query to proceed.</b>")
        return

    # Get the user query and mention
    user_query = message.text.split(maxsplit=1)[1]
    user_mention = message.from_user.mention

    # Simulate typing action before sending the response
    await send_typing_action(client, message.chat.id, duration=2)

    # Fetch the response from the AI API
    response = ask_query(user_query)

    # Send the formatted response
    await message.reply_text(
        f"{user_mention}, here’s what I found for you 🔍:\n\n<b>{response}</b>"
    )