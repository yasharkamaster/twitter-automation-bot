#!/usr/bin/env python3
"""
Debug script for Twitter API credentials
Run this to test your API credentials and permissions
"""

import os
import sys
from dotenv import load_dotenv
from twitter_bot import ProfessionalTwitterBot
from logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

def test_credentials():
    """Test Twitter API credentials"""
    logger.info("🚀 Starting Twitter API Credentials Test")
    logger.info("=" * 50)
    
    try:
        bot = ProfessionalTwitterBot()
        
        # Test API credentials
        success = bot.test_api_credentials()
        
        if success:
            logger.info("🎉 All tests passed! Your API credentials are working correctly.")
            return True
        else:
            logger.error("❌ API credentials test failed. Check the logs above for details.")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)
