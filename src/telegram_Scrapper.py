import asyncio
import nest_asyncio
import os
import re
from telethon import TelegramClient
import pytesseract
from PIL import Image
import unicodedata
import emoji
import nltk
from nltk.tokenize import word_tokenize
# from nltk.normalize import word_normalize
import pandas as pd


# Amharic text processing functions
def amharic_tokenize(text):
    """Tokenize Amharic text, handling Ethiopic script."""
    text = re.sub(r'\s+', ' ', text)
    tokens = word_tokenize(text)
    return str(tokens)  # Convert to string for CSV storage


def normalize_amharic(text):
    """Normalize Amharic text, removing emojis and standardizing characters."""
    text = emoji.replace_emoji(text, replace='')
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'[^\u1200-\u137F\s.,!?]', '', text)
    return text.strip()


def extract_image_text(image_path):
    """Extract text from images using Tesseract OCR with Amharic support."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='amh')
        return normalize_amharic(text)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""


async def scrape_channel(client, channel_handle, output_dir):
    """Scrape messages from a Telegram channel and save to CSV."""
    try:
        entity = await client.get_entity(channel_handle)
        channel_name = entity.title.replace(
            '/', '_')  # Sanitize for file paths
        os.makedirs(os.path.join(output_dir, channel_name), exist_ok=True)

        structured_data = []

        # Fetch messages (limit to 100 for testing; adjust for production)
        async for message in client.iter_messages(entity, limit=100):
            if message.message or message.media:
                data = {
                    "channel": channel_name,
                    "message_id": message.id,
                    "sender_id": message.sender_id or '',
                    "timestamp": message.date.isoformat(),
                    "text": "",
                    "tokens": "",
                    "image_text": "",
                    "media_path": ""
                }

                # Process text
                if message.message:
                    text = normalize_amharic(message.message)
                    data["text"] = text
                    data["tokens"] = amharic_tokenize(text)

                # Process media (images)
                if message.media and hasattr(message.media, 'photo'):
                    media_path = os.path.join(
                        output_dir, channel_name, f"image_{message.id}.jpg")
                    await client.download_media(message.media, media_path)
                    data["media_path"] = media_path
                    data["image_text"] = extract_image_text(media_path)

                structured_data.append(data)

        # Save structured data to CSV
        csv_path = os.path.join(output_dir, f"{channel_name}_data.csv")
        df = pd.DataFrame(structured_data)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Data from {channel_name} saved to {csv_path}")

    except Exception as e:
        print(f"Error processing {channel_handle}: {e}")


async def main():
    # Telegram API credentials (replace with your own)
    api_id = '29992189'  # Obtain from my.telegram.org
    api_hash = 'f234baf39ded2ba05973aba75d9b9f71'
    phone = '+251996665090'

    # Output directory
    output_dir = 'telegram_scraped_data'
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
