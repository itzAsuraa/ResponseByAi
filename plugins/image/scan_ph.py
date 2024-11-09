import requests
from Mangandi import ImageUploader
from pyrogram import Client, filters
from info import *
from database import *

api = "https://horridapi.onrender.com/search"

@Client.on_message(filters.command("scan_ph"))
async def scan_ph(client, message):
    if FSUB and not await get_fsub(client, message):
        return

    reply = message.reply_to_message    
    if not reply:
        return await message.reply_text("📸 Please reply to a photo to use this command!")
    elif not reply.photo:
        return await message.reply_text("📸 The replied message is not a photo!")
    elif reply.video:
        return await message.reply_text("📸 Please reply to a photo, not a video!")

    query = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""    
    if not query:
        return await message.reply_text("❗ Please provide a query! For example: `/scan_ph tell me about this image`")

    k = await message.reply_text(f"🔍 {message.from_user.mention}, Please wait while I check...")

    try:
        media = await reply.download()

        m = await k.edit("✅ Successfully downloaded the image, now checking your query...")

        # Create an ImageUploader instance
        mag = ImageUploader(media)

        # Upload the image and get the URL
        img_url = mag.upload()

        # Make the API request
        response = requests.get(f"{api}?img={img_url}&query={query}")

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            await m.edit(f"👤 {message.from_user.mention}, here's what I found: {result['response']}")
        else:
            await m.edit("⚠️ There was an error processing your request. Please try again later.")
    except Exception as e:
        await m.edit("❌ **An error occurred while processing your request.**")
        print(f"Error: {e}")  # Log the error for debugging