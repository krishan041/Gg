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
from vars import API_ID, API_HASH, BOT_TOKEN
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
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

API_ID    = os.environ.get("API_ID", "24495656")
API_HASH  = os.environ.get("API_HASH", "61afcf68c6429714dd18acd07f246571")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7842202956:AAHgKbWG5FSQhRdcovXmqaEYlPMd-dQu630") 

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

import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/sanjaykagra86"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/SSC_Aspirants_7"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/SSC_Aspirants_7"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/sanjaykagra86"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/SSC_Aspirants_7"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/SSC_Aspirants_7"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://i.ibb.co/dpRKmmj/file-3957.jpg",
    "https://i.ibb.co/NSbPQ5n/file-3956.jpg",
    "https://i.ibb.co/Z8R4z0g/file-3962.jpg",
    "https://i.ibb.co/LtqjVy7/file-3958.jpg",
    "https://i.ibb.co/bm20zfd/file-3959.jpg",
    "https://i.ibb.co/0V0BngV/file-3960.jpg",
    "https://i.ibb.co/rQMXQjX/file-3961.jpg",
    # Add more image URLs as needed
]

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        "**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 👋!**\n\n"
        "➠ **𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️**\n"
        "➠ **Can Extract Videos & PDFs From Your Text File and Upload to Telegram!**\n"
        "➠ **For Guide Use Command /guide 📖**\n\n"
        "➠ **Use /moni Command to Download From TXT File** 📄\n\n"
        "➠ **𝐌𝐚𝐝𝐞 𝐁𝐲:** @SanjayKagra86🩷"
    )

    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()


COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    """
    Command: /cookies
    Allows any user to upload a cookies file dynamically.
    """
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

# File paths
CHANNELS_FILE = "channels_data.json"

# Function to read channels data
def read_channels_data():
    if not os.path.exists(CHANNELS_FILE):
        return []
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)

# Function to write channels data
def write_channels_data(data):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# How to use:-
@bot.on_message(filters.command("guide"))
async def guide_handler(client: Client, message: Message):
    guide_text = (
        "🔑 **How to get started with Premium**:\n\n"
        "1. **First of all**, contact the owner and buy a premium plan. 💰\n"
        "2. **If you are a premium user**, you can check your plan by using `/myplan`. 🔍\n\n"
        "📖 **Usage**:\n\n"
        "1. `/add_channel -100{channel_id}` - Add a channel to the bot.\n"
        "2. `/remove_channel -100{channel_id}` - Remove a channel from the bot.\n"
        "3. `/moni .txt` file command - Process the .txt file.\n"
        "4. `/stop` - Stop the task running in the bot. 🚫\n\n"
        "If you have any questions, feel free to ask! 💬"
    )
    await message.reply_text(guide_text)

# 4. /add_channel
@bot.on_message(filters.command("add_channel"))
async def add_channel(client, message: Message):
    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id not in channels:
            channels.append(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} added.")
        else:
            await message.reply_text(f"Channel {channel_id} is already added.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /add_channel <channel_id>")

# 5. /remove_channels
@bot.on_message(filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id in channels:
            channels.remove(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} removed.")
        else:
            await message.reply_text(f"Channel {channel_id} is not in the list.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /remove_channels <channel_id>")

# Command to show all allowed channels (Admin only)
@bot.on_message(filters.command("allowed_channels"))
async def allowed_channels(client, message: Message):
    channels = read_channels_data()
    if channels:
        channels_list = "\n".join([f"- {channel}" for channel in channels])
        await message.reply_text(f"**📋 Allowed Channels:**\n\n{channels_list}")
    else:
        await message.reply_text("ℹ️ No channels are currently allowed.")

# Command to remove all channels (Admin only)
@bot.on_message(filters.command("remove_all_channels"))
async def remove_all_channels(client, message: Message):
    # Clear the channels data
    write_channels_data([])
    await message.reply_text("✅ **All channels have been removed successfully.**")

# 6. /stop
@bot.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    await message.reply_text("♦️ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ♦️", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("moni"))
async def moni_handler(client: Client, m: Message):
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
                    links.append(link)

        os.remove(x)
        print(len(links))

    except:
        await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
        if os.path.exists(x):
            os.remove(x)

    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐒𝐭𝐚𝐫𝐭 🔢**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)               

    # This is where you would set up your bot and connect the handle_command function      
    await editable.edit("**Enter Batch Name or send d for grabing from text filename.**")
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

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "visionias" in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsInN1YiI6IjYwYjAyNzY3ZDM2OWUwMDAyY2Q5ODNlYyIsImlzcyI6Imh0dHBzOi8vYXV0aDAuY29tLyIsImF1ZCI6Imh0dHBzOi8vYXBpLmNsYXNzcGx1c2FwcC5jb20iLCJpYXQiOjE2MzYwNjE0NzUsImV4cCI6MTYzNjA5NzQ3NSwiYXpwIjoib0lQYjRWb1F2dVdUVU1mV0NBR0l4d3pFZ2hUQWJXZ2NydGZQY1pNa1giLCJndHkiOiJwYXNzd29yZCJ9.4t_RP4GZfMy5E6Rk3U5s4h5m4d0yE1M3r6r4k1j4k5g'}).json().get("url")
                
            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if 'testbook' in url:
                id =  url.split("/")[-2]
                url =  "https://extractapi.vercel.app/classplus?link=https://cpvod.testbook.com/" + id + "/playlist.m3u8"

            elif 'cpvod.testbook' in url:
                id =  url.split("/")[-2]
                url =  "https://extractapi.vercel.app/classplus?link=https://cpvod.testbook.com/" + id + "/playlist.m3u8"
             
            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront
``
