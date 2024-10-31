from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from info import *

# Function to query the AI API
def ask_query(query, model='blackbox'):
    try:
        # Encode the query for URL safety
        encoded_query = urllib.parse.quote(query)
        url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

        # Make the request to the API
        response = requests.get(url)
        if response.status_code == 200:
            # Return the result if found, else give a fallback message
            return response.json().get("result", "Sorry, I couldn’t find a response.")
        else:
            return f"⚠️ Error fetching response from the API. Status code: {response.status_code}"
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {e}"

# Function to simulate typing action for a realistic experience
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Handler for the "/blackbox" command
@Client.on_message(filters.command("blackbox"))
async def handle_query(client, message):
    # Check if the user provided a query
    if len(message.command) < 2:
        await message.reply_text("<b>📝 Please enter a query to get started.</b>")
        return

    # Retrieve the user's query
    user_query = message.text.split(maxsplit=1)[1]
    user_mention = message.from_user.mention

    # Simulate typing action before sending response
    await send_typing_action(client, message.chat.id, duration=2)

    # Fetch the response from the AI API
    response = ask_query(user_query)

    # Construct the response message with user mention and response
    await message.reply_text(f"{user_mention}, <b>Here’s what I found:</b>\n\n{response}")