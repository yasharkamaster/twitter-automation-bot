import os
import sys
import logging
from datetime import datetime

def setup_logging():
    """Setup comprehensive logging for the Twitter bot"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    log_filename = f'logs/twitter_bot_{timestamp}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger
    logger = logging.getLogger('twitter_bot')
    
    # Log startup
    logger.info("=" * 50)
    logger.info("Twitter Bot Starting Up")
    logger.info(f"Log file: {log_filename}")
    logger.info("=" * 50)
    
    return logger

def log_tweet_activity(logger, content, success, tweet_id=None, error=None):
    """Log tweet posting activity"""
    if success:
        logger.info(f"✅ Tweet posted successfully - ID: {tweet_id}")
        logger.info(f"📝 Content: {content.get('title', 'N/A')[:100]}...")
        logger.info(f"📊 Source: {content.get('source', 'N/A')}")
    else:
        logger.error(f"❌ Failed to post tweet")
        if error:
            logger.error(f"🚨 Error: {error}")
        logger.error(f"📝 Content: {content.get('title', 'N/A')[:100]}...")

def log_content_scraping(logger, source, count):
    """Log content scraping activity"""
    logger.info(f"🔍 Scraped {count} items from {source}")

def log_rate_limit(logger, reset_time):
    """Log rate limit information"""
    logger.warning(f"⏰ Rate limit reached. Reset time: {reset_time}")

def cleanup_old_logs(days_to_keep=7):
    """Clean up old log files"""
    import glob
    import time
    
    current_time = time.time()
    cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
    
    log_files = glob.glob('logs/twitter_bot_*.log')
    
    for log_file in log_files:
        if os.path.getmtime(log_file) < cutoff_time:
            try:
                os.remove(log_file)
                print(f"Cleaned up old log file: {log_file}")
            except Exception as e:
                print(f"Error cleaning up {log_file}: {e}")
