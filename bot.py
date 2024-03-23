import os
import asyncio
from telegram import Bot
import subprocess
import json
from threading import Thread
import logging
import requests
import aiofiles


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load bot token and chat ID from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Previous balance for comparison, initialized as None
previous_balance = None

async def send_notification(message):
    """Send a notification via Telegram."""
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def get_balance():
    """Fetch the current balance using a HTTP request."""
    url = 'http://evmapp:9545/wallet/getTotalBalance'
    headers = {'accept': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        data = response.json()
        balance = data["result"]["balance"]
        return balance / 10**18
    except requests.RequestException as e:
        logger.error(f"Error getting balance from container: {e}")
    except (json.JSONDecodeError, KeyError):
        logger.error("Error parsing balance data.")
    return None

async def check_balance_change():
    """Check for balance changes and notify accordingly."""
    global previous_balance
    current_balance = await get_balance()
    if current_balance is not None and previous_balance is not None:
        balance_change = current_balance - previous_balance
        if balance_change != 0:
            change_type = "Received" if balance_change > 0 else "Sent out"
            await send_notification(f"{change_type} {abs(balance_change):.18f} amount. Current balance: {current_balance:.18f} ZEN")
    previous_balance = current_balance

async def balance_monitor():
    """Continuously check the balance every minute."""
    while True:
        await check_balance_change()
        await asyncio.sleep(60)  # Wait for 1 minute

async def follow_logs(filepath, term):
    """Follow the log file for new entries and send notifications for lines containing the term."""
    async with aiofiles.open(filepath, "r") as log_file:
        # Move to the end of the file
        await log_file.seek(0, os.SEEK_END)
        
        # Continuously check for new log entries
        while True:
            line = await log_file.readline()
            if line:
                if term in line:
                    await send_notification(line.strip())
            else:
                await asyncio.sleep(1)  # Wait for a second before checking for new log entries


async def main():
    # Attempt to fetch the initial balance at startup
    initial_balance = await get_balance()
    if initial_balance is not None:
        await send_notification(f"Bot started. Watching the logs for new forged blocks and monitoring for balance changes. Initial balance: {initial_balance:.18f} ZEN")
    else:
        await send_notification("Bot started, but unable to fetch initial balance.")

    # Define paths and terms
    log_file_path = '/app/logs/debug.log'
    term_to_watch = "forged"
    
    # Create tasks for log following and balance monitoring
    log_task = asyncio.create_task(follow_logs(log_file_path, term_to_watch))
    balance_task = asyncio.create_task(balance_monitor())

    # Wait for both tasks to complete (they're designed to run indefinitely)
    await asyncio.gather(log_task, balance_task)

if __name__ == "__main__":
    asyncio.run(main())
