# Professional Twitter Bot for Nexoxa

A sophisticated Twitter bot that automatically posts trending tech content every 2 hours, designed to boost your professional profile and showcase your expertise in building Nexoxa.

## Features

- **Automated Content Scraping**: Pulls trending tech news from Hacker News, TechCrunch, and Reddit
- **Professional Content Generation**: Uses pollinations.ai API to create engaging, professional tweets
- **Anti-Detection Measures**: Random delays and human-like behavior patterns
- **Image Support**: Downloads and posts relevant tech images (30% of tweets)
- **GitHub Actions Integration**: Fully automated posting via GitHub Actions
- **Professional Branding**: Mentions Nexoxa and your expertise throughout

## Setup

### 1. Twitter API Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app and get your API credentials
3. You'll need:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### 2. Environment Variables

1. Copy `env.example` to `.env`
2. Fill in your Twitter API credentials
3. Optionally add Unsplash API key for images

### 3. GitHub Secrets

Add these secrets to your GitHub repository:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `UNSPLASH_ACCESS_KEY` (optional)

## Usage

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot locally
python twitter_bot.py

# Run a single post (for testing)
python twitter_bot.py --single-post
```

### GitHub Actions

The bot automatically runs every 2 hours via GitHub Actions. You can also trigger it manually from the Actions tab.

## Content Strategy

The bot posts a mix of:

1. **Trending Tech News** (70%): Latest stories from Hacker News, TechCrunch, Reddit
2. **Professional Insights** (30%): Your own insights about building Nexoxa and startups

### Professional Insights Include:

- "get a status page, get a professional email, get a terms of service/privacy/policy, get a help center, get a blog, get a support twitter account - you instantly go from being another startup/saas to a real company"
- "wait fuck, i don't have a browser..." (the browser installation story)
- Various insights about programming, startups, and tech leadership

## Anti-Detection Features

- Random delays between 30-120 seconds before posting
- Human-like posting patterns
- Mix of text-only and image posts
- Professional, engaging content that doesn't look automated
- Proper error handling and logging

## File Structure

```
├── twitter_bot.py          # Main bot script
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── .github/
│   └── workflows/
│       └── twitter_bot.yml # GitHub Actions workflow
├── README.md              # This file
└── twitter_bot.log        # Bot logs (generated)
```

## Customization

### Adding New Content Sources

Edit the `get_trending_tech_content()` method to add new sources:

```python
def get_trending_tech_content(self) -> List[Dict]:
    content_sources = []
    
    # Add your new source here
    new_content = self._scrape_your_source()
    content_sources.extend(new_content)
    
    return content_sources
```

### Modifying Tweet Templates

Edit the `professional_templates` and `company_insights` lists in the `__init__` method.

### Changing Post Frequency

Modify the cron schedule in `.github/workflows/twitter_bot.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  - cron: '0 */4 * * *'  # Every 4 hours
```

## Monitoring

- Check `twitter_bot.log` for bot activity
- GitHub Actions logs show run history
- Twitter API rate limits are handled automatically

## Legal & Best Practices

- All content is properly attributed to sources
- Images are sourced from free-to-use APIs (Unsplash)
- Bot follows Twitter's automation rules
- Professional content that adds value to the community

## Support

This bot is designed to:
- Boost your professional profile
- Showcase your expertise with Nexoxa
- Engage with the tech community
- Build your personal brand

The content is professional, informative, and designed to position you as a thought leader in the tech space.

## License

This project is open source and available under the MIT License.
