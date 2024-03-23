# Simple Telegram Notification Bot for Zen EON Forger Node Monitoring

This project provides a simple Telegram bot designed to monitor your EVM-compatible blockchain node for new forged blocks. In addition to block monitoring, the bot keeps an eye on the node's wallet for any balance changes and sends notifications accordingly.

It is assumed your node was set up using: https://github.com/HorizenOfficial/compose-evm-simplified

## Features

- **Block Monitoring**: Automatically detects and notifies about new blocks forged by your node.
- **Balance Monitoring**: Watches for any changes in the node's wallet balance and sends notifications.

## Prerequisites

Before setting up the bot, you need to ensure that the `debug.log` file is enabled in your node's environment configuration. This file is essential for the bot to read and monitor the node's activity.

### Enabling `debug.log`

1. Open your node's `.env` file and locate the following line:
```
SCNODE_LOG_FILE_LEVEL=off
```

2. Change it to:
```
SCNODE_LOG_FILE_LEVEL=info
```

3. Save the changes and redeploy the EVM-compatible blockchain app Docker container.

### Finding the Log File

After enabling logging, locate the path to the `debug.log` file. For example:

/home/user/compose-evm-simplified/deployments/forger/eon/logs/evmapp/debug.log

Verify the log file is being written to (tail -f debug.log)


## Configuration

To configure the bot, you need to create a .env file in the bots directory with the following environment variables:

.env
```
TELEGRAM_BOT_TOKEN=your_bot_token_goes_here
TELEGRAM_CHAT_ID=your_chat_id_goes_here
DEBUG_LOG_DIR=/path/to/the/folder/with/debug.log/file/
```
Ensure you replace the placeholder values with your actual Telegram bot token, chat ID, and the path to your debug.log file.

## Running the Bot
To build and run the bot using Docker, execute the following command from the evmapp-telegram-bot directory:
```
sudo docker compose build && sudo docker compose up -d
```
