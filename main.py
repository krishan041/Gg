import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import datetime

from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
from core import download_and_send_video
import core as helper
from utils import progress_bar
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Initialize the bot
bot = Client(
    "bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

# Other parts of your code...

# Function to decode URL
def decode_url(encoded_url):
    return urllib.parse.unquote(encoded_url)

@bot.on_message(filters.command("moni"))
async def moni_handler(client: Client, m: Message):
    if m.chat.type == "private":
        user_id = str(m.from_user.id)
            
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍')

    try:
        input: Message = await client.listen(editable.chat.id)
        
        # Check if the message contains a document and is a .txt file
        if not input.document or not input.document.file_name.endswith('.txt'):
            await m.reply_text("Please send a valid .txt file.")
            return

        # Download the file
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"
        file_name = os.path.splitext(os.path.basename(x))[0]

        # Read and process the file
        with open(x, "r") as f:
            content = f.read().strip()

        lines = content.splitlines()
        links = []

        for line in lines:
            line = line.strip()
            if line:
                link = line.split("://", 1)
                if len(link) > 1:
                    decoded_link = decode_url(link[1])
                    links.append([link[0], decoded_link])

        os.remove(x)
        print(len(links))

    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")
        if os.path.exists(x):
            os.remove(x)

    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨[...]")

    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)               

    # This is where you would set up your bot and connect the handle_command function      
    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0
        
    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐑𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
        res = "UN"
    
    await editable.edit("**Enter Your Name or send `de` for use default**")

    # Listen for the user's response
    input3: Message = await bot.listen(editable.chat.id)

    # Get the raw text from the user's message
    raw_text3 = input3.text

    # Delete the user's message after reading it
    await input3.delete(True)

    # Default credit message
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'de':
        CR = '@SanjayKagra86🩷'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
   
    await editable.edit("🌄 Now send the Thumb url if don't want thumbnail send no ")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        # Assuming links is a list of lists and you want to process the second element of each sublist    
        for i in range(count - 1, len(links)):
            # Replace parts of the URL as needed
            V = links[i][1].replace("file/d/","uc?export=download&id=")\
               .replace("www.youtube-nocookie.com/embed", "youtu.be")\
               .replace("?modestbranding=1", "")\
               .replace("/view?usp=sharing","")\
               .replace("youtube.com/embed/", "youtube.com/watch?v=")

            url = "https://" + V

            # Construct yt-dlp command based on URL type
            cmd = construct_yt_dlp_command(url, name, raw_text2)

            # Execute the command
            res_file = await helper.download_video(url, cmd, name)
            filename = res_file
            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
            count += 1
            time.sleep(1)
    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")

# Function to handle different types of URLs and construct yt-dlp command
def construct_yt_dlp_command(url, name, quality):
    if "m3u8" in url:
        return f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={quality}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
    elif "youtube.com" in url or "youtu.be" in url:
        ytf = f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        return f'yt-dlp --cookies "youtube_cookies.txt" -f "{ytf}" "{url}" -o "{name}.mp4"'
    elif "embed" in url:
        ytf = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"
        return f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
    elif "mpd" in url:
        return f"yt-dlp -k --allow-unplayable-formats -f bestvideo[height<={quality}] --fixup never {url}"
    else:
        # Default command for other URLs
        ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"
        return f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

if __name__ == "__main__":
    try:
        bot.run()
    except Exception as e:
        print(f"Failed to start bot: {e}")
