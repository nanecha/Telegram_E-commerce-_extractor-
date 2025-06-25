import asyncio
import os
import re
from telethon import TelegramClient
import pytesseract
import nltk
# from nltk.normalize import word_normalize
import pandas as pd
from dotenv import load_dotenv
import nest_asyncio

# Load environment variables once
load_dotenv('api.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape data from a single channel


async def scrape_channel(client, channel_handle, output_dir):
    """
    Scrape messages from a Telegram channel and save to CSV while preserving
    emojis and symbols
    """
    try:
        entity = await client.get_entity(channel_handle)
        channel_name = entity.title.replace(
            '/', '_')  # Sanitize for file paths
        os.makedirs(os.path.join(output_dir, channel_name), exist_ok=True)

        structured_data = []

        async for message in client.iter_messages(entity, limit=400):
            if message.message or message.media:
                data = {
                    "channel": channel_name,
                    "message_id": message.id,
                    "sender_id": message.sender_id or '',
                    "timestamp": message.date.isoformat(),
                    "raw_text": (
                        message.message if message.message else ""
                    ),  # Keep original text
                    "text": (
                        clean_text_preserve_emoji(message.message)
                        if message.message else ""
                    ),
                    "tokens": "",
                    "image_text": "",
                    "media_path": ""
                }

                # Process media (images)
                if message.media and hasattr(message.media, 'photo'):
                    media_path = os.path.join(
                        output_dir, channel_name, f"image_{message.id}.jpg")
                    await client.download_media(message.media, media_path)
                    data["media_path"] = media_path

                structured_data.append(data)

        # Save with UTF-8 encoding to preserve all characters
        csv_path = os.path.join(output_dir, f"{channel_name}_data.csv")
        df = pd.DataFrame(structured_data)
        # Note: utf-8-sig preserves emojis
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Data from {channel_name} saved to {csv_path}")

    except Exception as e:
        print(f"Error processing {channel_handle}: {e}")


def clean_text_preserve_emoji(text):
    """Clean text while preserving emojis and symbols"""
    if not text:
        return ""
    # Only remove harmful characters, preserve most symbols and emojis
    # Remove control characters
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = text.strip()
    return text


async def main():
    # Telegram API credentials (replace with your own)
    # api_id = '29992189'  # Obtain from my.telegram.org
    # api_hash = 'f234baf39ded2ba05973aba75d9b9f71'
    # phone = '+2519966650
    # Output directory
    output_dir = 'telegram_scraped2_data'
    os.makedirs(output_dir, exist_ok=True)

    # List of Telegram channels to scrape
    channels = [
        '@Shageronlinestore',
        '@ZemenExpress',
        '@nevacomputer',
        '@sinayelj',
        '@Leyueqa'
    ]

    # Initialize Telegram client
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Authorize client
        await client.start(phone)
        print("Client connected successfully")

        # Scrape data from each channel
        for channel in channels:
            await scrape_channel(client, channel, output_dir)

# Download NLTK data for tokenization
nltk.download('punkt', quiet=True)
# Configure Tesseract path (update as needed)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Example path
nest_asyncio.apply()
asyncio.run(main())
asyncio.run(main())
