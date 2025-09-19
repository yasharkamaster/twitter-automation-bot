#!/usr/bin/env python3
"""
Simple runner script for the Professional Twitter Bot
"""

import sys
import os
from twitter_bot import ProfessionalTwitterBot
from logger import setup_logging

def main():
    """Main entry point"""
    logger = setup_logging()
    
    try:
        logger.info("🚀 Starting Professional Twitter Bot...")
        bot = ProfessionalTwitterBot()
        
        # Check if running in single-post mode (for GitHub Actions)
        if len(sys.argv) > 1 and sys.argv[1] == '--single-post':
            logger.info("📱 Running single post mode...")
            bot.run_scheduled_posts()
        else:
            logger.info("🔄 Starting continuous mode...")
            bot.start_bot()
            
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
