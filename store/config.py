"""
Configuration settings for the store application
"""
import os
from dotenv import load_dotenv

load_dotenv()

DISCOUNT_ORDER_INTERVAL = int(os.getenv('DISCOUNT_ORDER_INTERVAL', '3'))
DISCOUNT_PERCENTAGE = int(os.getenv('DISCOUNT_PERCENTAGE', '10'))