from pyrogram import Client, filters, enums
import requests, urllib.parse, asyncio
from pyrogram.types import Message
from info import *

# AI Response Function
def ask_query(query, model='gpt-4o'):
    """
    Query the AI API and retrieve a response.
    """
    system_prompt = ("""You are a helpful assistant. Your name is ResponseByAi, and your owner's name is Captain, known as @itzAsuraa. """
    )
    query = f"{system_prompt}\n\nUser: {query}"
    url = f"https://chatwithai.codesearch.workers.dev/?chat={urllib.parse.quote(query)}&model={model}"
    response = requests.get(url)
    return response.json().get("result", "No response found.") if response.status_code == 200 else f"Error: {response.status_code}"

# Simulate Typing Action
async def send_typing_action(client, chat_id, duration=1):
    """
    Simulate typing action.
    """
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# "/ask" Command Handler
@Client.on_message(filters.command("ask"))
async def handle_query(client, message):
    """
    Handle the /ask command.
    """
    if len(message.command) < 2:
        await message.reply_text("<b>📝 Please provide a query to ask ResponseByAi! Don't be shy, let's chat! 🤖💬</b>")
        return

    user_query = message.text.split(maxsplit=1)[1]
    user_mention = message.from_user.mention

    # Simulate typing, then send AI response
    await send_typing_action(client, message.chat.id, duration=2)
    response = ask_query(user_query)
    await message.reply_text(f"{user_mention}, <b>{response}</b> 🚀")

# Mention Handler for Group Chats
@Client.on_message(filters.mentioned & filters.group)
async def handle_mention(client: Client, message: Message):
    """
    Respond to mentions in group chats.
    """
    user_text = message.reply_to_message.text.strip() if message.reply_to_message and message.reply_to_message.text else message.text.split(" ", 1)[1].strip()

    if user_text:
        model_name = get_model_from_db(message.chat.id)
        await send_typing_action(client, message.chat.id)
        api_response = ask_query(user_text, model_name)
        await message.reply(f"🤖 <b>{api_response}</b>")
    else:
        await message.reply("<b>👋 Please ask a question after mentioning me! I’m here to help! 😊</b>")
        