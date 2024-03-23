FROM python:3.9-slim

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
RUN pip install python-telegram-bot requests aiofiles

# Copy bot script into the container
COPY bot.py .

# Run the bot script
CMD ["python", "./bot.py"]
