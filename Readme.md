Simple Telegram notification bot to monitor your evmapp node for new forged blocks.

At the same time it monitors the node's wallet for balance changes and sends a notification when a change occurs.

The bot need to read the debug.log file. The file has to be enabled first in your evmapp .env file:

Change:
SCNODE_LOG_FILE_LEVEL=off
to
SCNODE_LOG_FILE_LEVEL=info

and redeploy the evmapp docker container.

Find the path to the log file, example:
/home/user/compose-evm-simplified/deployments/forger/eon/logs/evmapp/debug.log

.env file:

TELEGRAM_BOT_TOKEN=your_bot_token_goes_here
TELEGRAM_CHAT_ID=your_chat_id_goes here
DEBUG_LOG_DIR=/path/to/the/folder/with/debug.log/file/

To run the bot:
docker compose build && docker compose up -d
