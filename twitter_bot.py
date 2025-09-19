import os
import tweepy
import requests
import time
import random
import json
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import schedule
import logging
from typing import List, Dict, Optional
import urllib.parse
from PIL import Image
import io
from logger import setup_logging, log_tweet_activity, log_content_scraping, cleanup_old_logs

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

class ProfessionalTwitterBot:
    def __init__(self):
        """Initialize the professional Twitter bot with API credentials"""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials in environment variables")
        
        # Initialize Twitter API v2
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Initialize API v1.1 for media uploads
        self.auth = tweepy.OAuth1UserHandler(
            self.api_key, self.api_secret,
            self.access_token, self.access_token_secret
        )
        self.api_v1 = tweepy.API(self.auth)
        
        # Professional content templates
        self.professional_templates = [
            "Building Nexoxa taught me: {insight}\n\nWhat's your take on this? #TechLeadership #StartupLife #Nexoxa #AIContent",
            "After creating Nexoxa (AI content sharing platform), I've learned: {insight}\n\nAlways evolving in tech! #Innovation #TechTrends #Nexoxa",
            "From building Nexoxa: {insight}\n\nThoughts? #TechCommunity #Entrepreneurship #AIContent #Nexoxa",
            "Creating Nexoxa showed me: {insight}\n\nTech never stops amazing me! #TechNews #FutureTech #Nexoxa #Innovation",
            "Nexoxa development insight: {insight}\n\nAgree or disagree? #TechDebate #Programming #AIContent #Nexoxa"
        ]
        
        # Professional insights about building companies and Nexoxa
        self.company_insights = [
            "get a status page\nget a professional email\nget a terms of service/privacy/policy\nget a help center\nget a blog\nget a support twitter account\n\nyou instantly go from being another startup/saas to a real company",
            "wait fuck, i don't have a browser\n\nim setting up this new pc\n\nfirst thing i do, i uninstall microsoft edge\n\nthen i realize\n\ni don't have any other browser\n\nso now i can't get a browser\n\ni cant install a browser without a browser\n\nplease help",
            "Revamped an old TV into a sleek, vintage-inspired gift—combining nostalgia with modern tech! 🚀💡 Proud to have built Nexoxa, pushing boundaries in creative tech solutions. Who else loves giving new life to old devices? #TechRevamp #DIY #Innovation #Nexoxa #Gifts #TechTips",
            "Building Nexoxa taught me: the best way to learn programming is to build something you actually want to use",
            "Nexoxa is an AI content sharing platform that revolutionizes how creators share and discover content. Most startups fail not because of bad code, but because of bad product-market fit",
            "The hardest part of building Nexoxa wasn't the technical challenges, it's the people problems",
            "Every successful tech company like Nexoxa started with someone solving their own problem",
            "The best developers aren't the ones who know every language, they're the ones who can learn any language - learned this building Nexoxa",
            "Code reviews aren't about finding bugs, they're about knowledge sharing and team growth - essential for Nexoxa's success",
            "Building Nexoxa taught me: the most important skill in tech isn't coding, it's communication",
            "Creating Nexoxa showed me: building a startup is 10% coding and 90% everything else"
        ]
        
        logger.info("Professional Twitter bot initialized successfully")
    
    def get_trending_tech_content(self) -> List[Dict]:
        """Scrape trending tech content from various sources"""
        content_sources = []
        
        try:
            # Hacker News
            hn_content = self._scrape_hacker_news()
            content_sources.extend(hn_content)
            
            # TechCrunch RSS
            tc_content = self._scrape_techcrunch_rss()
            content_sources.extend(tc_content)
            
            # Reddit r/programming
            reddit_content = self._scrape_reddit_programming()
            content_sources.extend(reddit_content)
            
            # Add professional insights
            insight_content = self._get_professional_insights()
            content_sources.extend(insight_content)
            
            log_content_scraping(logger, "All Sources", len(content_sources))
            return content_sources
            
        except Exception as e:
            logger.error(f"Error scraping content: {e}")
            return []
    
    def _get_professional_insights(self) -> List[Dict]:
        """Generate professional insights about building companies and tech"""
        insights = []
        
        for insight in self.company_insights:
            insights.append({
                'title': insight,
                'url': '',
                'source': 'Nexoxa Insights',
                'timestamp': datetime.now(),
                'type': 'professional_insight'
            })
        
        return insights
    
    def _scrape_hacker_news(self) -> List[Dict]:
        """Scrape top stories from Hacker News"""
        try:
            response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
            story_ids = response.json()[:10]  # Top 10 stories
            
            stories = []
            for story_id in story_ids:
                story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
                story = story_response.json()
                
                if story and story.get('type') == 'story' and story.get('title'):
                    stories.append({
                        'title': story['title'],
                        'url': story.get('url', ''),
                        'score': story.get('score', 0),
                        'source': 'Hacker News',
                        'timestamp': datetime.now(),
                        'type': 'news'
                    })
            
            return stories
            
        except Exception as e:
            logger.error(f"Error scraping Hacker News: {e}")
            return []
    
    def _scrape_techcrunch_rss(self) -> List[Dict]:
        """Scrape latest articles from TechCrunch RSS"""
        try:
            import feedparser
            feed = feedparser.parse('https://techcrunch.com/feed/')
            
            articles = []
            for entry in feed.entries[:5]:  # Latest 5 articles
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'summary': entry.get('summary', ''),
                    'source': 'TechCrunch',
                    'timestamp': datetime.now(),
                    'type': 'news'
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping TechCrunch: {e}")
            return []
    
    def _scrape_reddit_programming(self) -> List[Dict]:
        """Scrape hot posts from r/programming"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(
                'https://www.reddit.com/r/programming/hot.json',
                headers=headers,
                timeout=10
            )
            
            # Check if response is valid
            if response.status_code != 200:
                logger.warning(f"Reddit API returned status code: {response.status_code}")
                return []
            
            # Check if response has content
            if not response.text.strip():
                logger.warning("Reddit API returned empty response")
                return []
            
            try:
                data = response.json()
            except ValueError as e:
                logger.warning(f"Reddit API returned invalid JSON: {e}")
                return []
            
            # Check if data structure is valid
            if 'data' not in data or 'children' not in data['data']:
                logger.warning("Reddit API returned unexpected data structure")
                return []
            
            posts = []
            for post in data['data']['children'][:5]:  # Top 5 posts
                if 'data' in post:
                    post_data = post['data']
                    posts.append({
                        'title': post_data.get('title', 'No title'),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'source': 'Reddit r/programming',
                        'timestamp': datetime.now(),
                        'type': 'discussion'
                    })
            
            return posts
            
        except requests.exceptions.Timeout:
            logger.warning("Reddit API request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.warning(f"Reddit API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
            return []
    
    def format_tweet_with_pollinations(self, content: Dict) -> str:
        """Use pollinations.ai to format tweet content"""
        try:
            # Create a prompt for pollinations.ai
            if content.get('type') == 'professional_insight':
                prompt = f"Create a Twitter post about this tech insight: {content['title']}. Make it engaging, professional, and mention that I built Nexoxa (an AI content sharing platform). Include relevant hashtags. Keep it under 280 characters. Format with proper line breaks for readability."
            else:
                prompt = f"Create a Twitter post about this tech topic: {content['title']}. Make it engaging, informative, and professional. Mention that I built Nexoxa (an AI content sharing platform). Include relevant hashtags. Keep it under 280 characters. Format with proper line breaks for readability."
            
            # Encode the prompt for URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Call pollinations.ai API
            response = requests.get(f'https://text.pollinations.ai/{encoded_prompt}')
            
            if response.status_code == 200:
                formatted_text = response.text.strip()
                
                # Ensure it's under 280 characters
                if len(formatted_text) > 280:
                    formatted_text = formatted_text[:277] + "..."
                
                return formatted_text
            else:
                # Fallback to manual formatting
                return self._manual_format_tweet(content)
                
        except Exception as e:
            logger.error(f"Error formatting with pollinations.ai: {e}")
            return self._manual_format_tweet(content)
    
    def _manual_format_tweet(self, content: Dict) -> str:
        """Manual tweet formatting as fallback"""
        title = content['title']
        source = content['source']
        
        if content.get('type') == 'professional_insight':
            # Use professional templates for insights
            template = random.choice(self.professional_templates)
            tweet = template.format(insight=title)
        else:
            # Create engaging tweet formats for news
            tweet_templates = [
                f"🔥 {title}\n\nBuilding Nexoxa (AI content sharing platform) taught me to stay updated with tech trends! #TechNews #Programming #Nexoxa #AIContent",
                f"Interesting read: {title}\n\nAlways learning something new in tech! #TechTrends #Innovation #Nexoxa",
                f"Just came across this: {title}\n\nThoughts? #TechCommunity #Nexoxa #StartupLife #AIContent",
                f"📰 {title}\n\nTech never stops evolving! #TechNews #FutureTech #Nexoxa #Innovation",
                f"Hot take: {title}\n\nAgree or disagree? #TechDebate #Programming #Nexoxa #AIContent"
            ]
            tweet = random.choice(tweet_templates)
        
        # Ensure it fits Twitter's character limit
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return tweet
    
    def download_tech_image(self) -> Optional[str]:
        """Download a free-to-use tech-related image"""
        try:
            # Use Unsplash API for free images
            unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY')
            
            if unsplash_access_key:
                # Search for tech-related images
                tech_keywords = ['technology', 'programming', 'coding', 'software', 'computer', 'ai', 'tech', 'startup', 'business']
                keyword = random.choice(tech_keywords)
                
                response = requests.get(
                    f'https://api.unsplash.com/photos/random',
                    params={
                        'query': keyword,
                        'orientation': 'landscape',
                        'client_id': unsplash_access_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data['urls']['regular']
                    
                    # Download image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        # Save image temporarily
                        image_path = f"temp_image_{int(time.time())}.jpg"
                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        # Resize image for Twitter (max 5MB, optimal size)
                        self._resize_image_for_twitter(image_path)
                        return image_path
            
            return None
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None
    
    def _resize_image_for_twitter(self, image_path: str):
        """Resize image to optimal Twitter dimensions"""
        try:
            with Image.open(image_path) as img:
                # Twitter optimal size: 1200x675 or smaller
                max_size = (1200, 675)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(image_path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
    
    def post_tweet(self, content: Dict, include_image: bool = False):
        """Post a tweet with optional image"""
        try:
            # Format the tweet content
            tweet_text = self.format_tweet_with_pollinations(content)
            
            # Add random delay to appear more human-like
            delay = random.uniform(30, 120)  # 30 seconds to 2 minutes
            logger.info(f"Waiting {delay:.1f} seconds before posting...")
            time.sleep(delay)
            
            if include_image:
                # Download and upload image
                image_path = self.download_tech_image()
                
                if image_path:
                    try:
                        # Upload media using API v1.1
                        media = self.api_v1.media_upload(image_path)
                        
                        # Post tweet with image
                        response = self.client.create_tweet(
                            text=tweet_text,
                            media_ids=[media.media_id]
                        )
                        
                        logger.info(f"Posted tweet with image: {response.data['id']}")
                        
                        # Clean up temporary image
                        os.remove(image_path)
                        
                    except Exception as e:
                        logger.error(f"Error posting with image: {e}")
                        # Fallback to text-only tweet
                        response = self.client.create_tweet(text=tweet_text)
                        logger.info(f"Posted text-only tweet: {response.data['id']}")
                else:
                    # No image available, post text-only
                    response = self.client.create_tweet(text=tweet_text)
                    logger.info(f"Posted text-only tweet: {response.data['id']}")
            else:
                # Post text-only tweet
                response = self.client.create_tweet(text=tweet_text)
                logger.info(f"Posted tweet: {response.data['id']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
    
    def run_scheduled_posts(self):
        """Run the bot's scheduled posting routine"""
        logger.info("Starting scheduled posting routine...")
        
        # Get trending content
        content_items = self.get_trending_tech_content()
        
        if not content_items:
            logger.warning("No content found, skipping this round")
            return
        
        # Select random content item
        selected_content = random.choice(content_items)
        
        # Randomly decide whether to include image (30% chance)
        include_image = random.random() < 0.3
        
        # Post the tweet
        success = self.post_tweet(selected_content, include_image)
        
        if success:
            log_tweet_activity(logger, selected_content, True)
        else:
            log_tweet_activity(logger, selected_content, False)
    
    def start_bot(self, single_post: bool = False):
        """Start the bot with scheduled posting"""
        logger.info("Starting Professional Twitter bot...")
        
        if single_post:
            # Run once for GitHub Actions
            logger.info("Running single post...")
            self.run_scheduled_posts()
        else:
            # Schedule posts every 2 hours
            schedule.every(2).hours.do(self.run_scheduled_posts)
            
            # Run once immediately for testing
            logger.info("Running initial post...")
            self.run_scheduled_posts()
            
            # Keep the bot running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Professional Twitter Bot')
    parser.add_argument('--single-post', action='store_true', help='Run a single post (for GitHub Actions)')
    args = parser.parse_args()
    
    try:
        bot = ProfessionalTwitterBot()
        bot.start_bot(single_post=args.single_post)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")