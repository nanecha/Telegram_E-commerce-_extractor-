# Building an Amharic E-commerce Data Extractor
# Task-1  Data Ingestion and Preprocessing for Ethiopian Telegram E-commerce Channels
## Overview
This project implements Task 1 of the data pipeline for collecting and preprocessing data from Ethiopian-based Telegram e-commerce channels for Named Entity Recognition (NER). The script scrapes messages (text, images, and metadata) from specified Telegram channels, preprocesses Amharic text, extracts text from images using OCR, and saves the structured data to CSV files. The system is designed to handle Amharic-specific linguistic features and prepare data for subsequent NER labeling and model fine-tuning.
# setups and Dependencies
- See requirements.txt

## Objectives
- Set up a data ingestion system to fetch messages from at least five Ethiopian e-commerce Telegram channels.
- Preprocess Amharic text by tokenizing, normalizing, and handling Ethiopic script features.
- Store preprocessed data in CSV files for further analysis.

*The following Telegram channels were selected for data ingestion:*
- @Shageronlinestore 
- @ZemenExpress 
- @nevacomputer 
- @sinayelj 
- @Leyueqa 

*Telegram API Credentials:* 
- Obtain api_id and api_hash from my.telegram.org.
## Usage
- Prepare the script:

- Ensure the script (telegram_channel_scraper_csv.py) has the correct API credentials and Tesseract path.
Verify that your Telegram account has joined the target channels (if private).
Run the script:

- Directory: telegram_scraped_data/
Subdirectories for each channel (e.g., Shager Online Store/) contain images.
CSV files (e.g., Shager_Online_Store_data.csv) store structured data.

