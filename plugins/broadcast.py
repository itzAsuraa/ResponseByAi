from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import *
from info import *

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(OWNER_ID))
async def broadcasting_func(client, message):
    if message.from_user.id != OWNER_ID:
        return

    count = 0
    failed = 0

    # Extract the broadcast message text
    broadcast_text = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )

    if not broadcast_text:
        return await message.reply_text("❌ Please provide a caption for the broadcast.")

    # Notify that the broadcast has started
    bmsg = await message.reply_text(text=f"🚀 Broadcast Started for:\n\n{broadcast_text}")

    # Check if the broadcast is for an audio message
    if message.reply_to_message and message.reply_to_message.audio:
        audio_message = message.reply_to_message.audio
        audio_file_id = audio_message.file_id

        bmsg = await bmsg.edit(f"📢 Broadcasting audio with caption:\n\n<b>{broadcast_text}</b>")

        for userDoc in userList.find():
            userId = userDoc["userId"]
            try:
                await client.send_audio(
                    userId,
                    audio_file_id,
                    caption=f"🎶 <b>{broadcast_text}</b>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton(
                                "🛠️ Admin Support",
                                url="https://t.me/AsuraaSupports",
                            )
                        ]]
                    ),
                )
                count += 1

                # Update progress every 20 broadcasts
                if count % 20 == 0:
                    await bmsg.edit(f"📈 Broadcasted to {count} users... \n❌ Failed: {failed}")
            except Exception as e:
                failed += 1
                print(f"🚫 Error while broadcasting audio: {e}")

    else:
        bmsg = await bmsg.edit(f"📝 Broadcasting message:\n\n<b>{broadcast_text}</b>")

        for userDoc in userList.find():
            userId = userDoc["userId"]
            try:
                await client.send_message(
                    userId,
                    text=f"🗣️ <b>{broadcast_text}</b>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton(
                                "🛠️ Admin Support",
                                url="https://t.me/AsuraaSupports",
                            )
                        ]]
                    ),
                )
                count += 1

                # Update progress every 20 broadcasts
                if count % 20 == 0:
                    await bmsg.edit(f"📈 Broadcasted to {count} users... \n❌ Failed: {failed}")
            except Exception as e:
                failed += 1
                print(f"🚫 Error while broadcasting message: {e}")

    # Final update on broadcast status
    await bmsg.edit(f"✅ Successfully broadcasted to {count} users...\n❌ Failed: {failed}")