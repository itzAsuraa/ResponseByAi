from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from info import *

# Function to query the AI API
def ask_query(query, model='gemini'):
    try:
        # Encode the user query for safe URL handling
        encoded_query = urllib.parse.quote(query)
        url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

        # Send the request to the API
        response = requests.get(url)
        if response.status_code == 200:
            # Return the response or a fallback message if no result is found
            return response.json().get("result", "I couldn't find an answer to that.")
        else:
            return f"⚠️ Could not retrieve data from the API. (Status code: {response.status_code})"
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {e}"

# Function to simulate typing action for an enhanced user experience
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Handler for the "/gemini" command
@Client.on_message(filters.command("gemini"))
async def handle_query(client, message):
    # Check if a query was provided by the user
    if len(message.command) < 2:
        await message.reply_text("💡 <b>Kindly provide a question to proceed.</b>")
        return

    # Get the user's question and mention
    user_query = message.text.split(maxsplit=1)[1]
    user_mention = message.from_user.mention

    # Simulate typing to enhance the user experience
    await send_typing_action(client, message.chat.id, duration=2)

    # Query the AI API for a response
    response = ask_query(user_query)

    # Send the response with user mention
    await message.reply_text(
        f"{user_mention}, here’s what I found for you:\n\n<b>{response}</b>"
    )