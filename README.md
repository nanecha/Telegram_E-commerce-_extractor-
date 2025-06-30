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

# 📌 Task 2: Label Data Subset in CoNLL Format

This task focuses on building a Named Entity Recognition (NER) dataset for Amharic product descriptions collected from Telegram e-commerce channels. The goal is to preprocess, label, and export the data in CoNLL format for use in NER model training or fine-tuning.
 
## 🔹 Import Custom Preprocessing Functions

Custom functions for Amharic text normalization and tokenization

from src.preprocessing_labelling import normalize_amharic_text, tokenize_amharic_text

## 🔹 Define Keywords for Labelling
Keyword sets used to identify and tag entities with BIO labels:

product_keywords = {
    'ስማርትፎን', 'ጫማ', 'ቦርሳ', 'ላፕቶፕ', 'ቲሸርት', 'ቀሚስ', 'ሰዓት', 'ካሜራ',
    'ማዳመጫ', 'ብስክሌት', 'ልብስ', 'ማቀዝቀዣ', 'ቡታ', 'ጥፍር', 'መጠጥ', 'ልጅ',
    'መቀቀል', 'መገጣጠሚያ', 'ተብሌት', 'መጫወቻ', 'ምድጃ', 'ሶፋ', 'መጽሐፍ',
    'ሞባይል', 'ጠረጴዛ', 'ጃኬት', 'ሰንሰለት', 'ባትሪ'
}
location_keywords = {'አዲስ_አበባ', 'ቦሌ', 'ፒያሳ', 'መገናኛ', 'ሜክሲኮ',
                     'አራት_ኪሎ', 'ጎፋ', 'ለገሃር', 'ቦታ', 'ቢሮ', 'አድራሻ'}
price_keywords = {'በ', 'ዋጋ', 'ብር'}

## 🔹 Apply Labeling Function

##💾 Export as CoNLL File 

This file can used the Task-1

## ⚙️ Workflow Insight
The pipeline follows four structured stages:


1. Data Loading	: Reads cleaned product descriptions from CSV

2. Tokenization & Normalization	:Cleans Amharic text and splits into linguistically meaningful tokens

3. Rule-based Labeling	:Uses keyword dictionaries to assign BIO entity labels

4. CoNLL Export	:Saves labeled data in standard format for training NER models

✅ The design is modular and easy to integrate into further model training or evaluation stages.
Key Observations:
⚠️ Most tokens are labeled as O, meaning they're outside any predefined entity.

## 🔎 This highlights:

Limited keyword coverage.

Missed entities such as brand names or non-keyword locations.

A potential need to expand keyword dictionaries or use semi-supervised labeling methods.