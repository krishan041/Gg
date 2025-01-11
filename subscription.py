import os
import json
import hashlib
import hmac
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize the bot
bot = Client(
    "subscription_bot",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

# File paths
SUBSCRIPTIONS_FILE = "subscriptions_data.json"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

# Function to read subscriptions data
def read_subscriptions_data():
    if not os.path.exists(SUBSCRIPTIONS_FILE):
        return []
    with open(SUBSCRIPTIONS_FILE, "r") as f:
        return json.load(f)

# Function to write subscriptions data
def write_subscriptions_data(data):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Function to generate HMAC signature
def generate_signature(data):
    return hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()

# Function to verify HMAC signature
def verify_signature(data, signature):
    return hmac.compare_digest(generate_signature(data), signature)

# Command to show all subscriptions
@bot.on_message(filters.command("subscriptions"))
async def subscriptions(client, message: Message):
    subscriptions = read_subscriptions_data()
    if subscriptions:
        subscriptions_list = "\n".join([f"- {subscription['user_id']} (Free)" for subscription in subscriptions])
        await message.reply_text(f"**📋 Subscriptions:**\n\n{subscriptions_list}")
    else:
        await message.reply_text("ℹ️ No subscriptions are currently available.")

# Command to add a free subscription for a user
@bot.on_message(filters.command("add_subscription"))
async def add_subscription(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscriptions = read_subscriptions_data()
        data = f"{user_id}:Free"
        signature = generate_signature(data)
        subscriptions.append({"user_id": user_id, "type": "Free", "signature": signature})
        write_subscriptions_data(subscriptions)
        await message.reply_text(f"Free subscription for user {user_id} added.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /add_subscription <user_id>")

# Command to verify a free subscription
@bot.on_message(filters.command("verify_subscription"))
async def verify_subscription(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscriptions = read_subscriptions_data()
        for subscription in subscriptions:
            if subscription["user_id"] == user_id:
                data = f"{user_id}:Free"
                if verify_signature(data, subscription["signature"]):
                    await message.reply_text(f"Subscription for user {user_id} is valid and free.")
                else:
                    await message.reply_text(f"Subscription for user {user_id} is invalid.")
                return
        await message.reply_text(f"No subscription found for user {user_id}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /verify_subscription <user_id>")

# Command to remove a subscription
@bot.on_message(filters.command("remove_subscription"))
async def remove_subscription(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscriptions = read_subscriptions_data()
        subscriptions = [sub for sub in subscriptions if sub["user_id"] != user_id]
        write_subscriptions_data(subscriptions)
        await message.reply_text(f"Subscription for user {user_id} removed.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /remove_subscription <user_id>")

# Command to remove all subscriptions
@bot.on_message(filters.command("remove_all_subscriptions"))
async def remove_all_subscriptions(client, message: Message):
    # Clear the subscriptions data
    write_subscriptions_data([])
    await message.reply_text("✅ **All subscriptions have been removed successfully.**")

bot.run()
