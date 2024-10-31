from pyrogram import Client, filters
import requests
from info import *

# Generate a detailed prompt for image creation
def generate_long_query(query):
    base_query = f"{query}."
    return base_query

@Client.on_message(filters.command("draw"))
async def draw_image(client, message):
    if len(message.command) < 2:
        await message.reply_text("**Please provide a query to generate an image.** 😊")
        return

    # Generate a long query for better image results
    user_query = message.text.split(" ", 1)[1]
    query = generate_long_query(user_query)

    # Send initial message
    wait_message = await message.reply_text("**Generating image, please wait...** ⏳")

    # Generate image URL using the API
    url = f"https://text2img.codesearch.workers.dev/?prompt={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.json()
            image_url = image_data.get("image")
            if image_url:
                # Delete the wait message
                await wait_message.delete()
                # Send the generated image
                await message.reply_photo(photo=image_url, caption=f"**Generated Image for: {user_query}** 🖼️")
            else:
                await wait_message.edit_text("Failed to retrieve image URL. Please try again. ❌")
        else:
            await wait_message.edit_text("Error: Unable to generate image at this time. Please try later. 🚫")
    except Exception as e:
        await wait_message.edit_text(f"An error occurred: {e} ⚠️")