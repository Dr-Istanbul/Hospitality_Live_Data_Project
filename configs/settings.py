# configs/settings.py
import os

# AWS Settings
AWS_REGION = "us-east-1"
S3_BUCKET = "dallas-data-pipeline"

# Project Settings
DATA_SOURCES = {
    "restaurants": ["opentable", "resy", "tock"],
    "causes": ["irs", "school_directories", "church_directories"], 
    "creators": ["instagram_hashtags", "tiktok_hashtags"]
}

# Output Schema
RESTAURANT_SCHEMA = [
    "name", "address", "phone", "website", "reservation_platform", 
    "reservation_url", "price_band", "cuisine_tags", "neighborhood",
    "lat", "lng", "hours", "avg_check_estimate", "rating", "review_count",
    "image_url", "menu_url", "source_platform"
]