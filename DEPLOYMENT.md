# Deployment Guide for Professional Twitter Bot

## Quick Start

### 1. Fork/Clone Repository
```bash
git clone https://github.com/yourusername/twitter-automation-bot.git
cd twitter-automation-bot
```

### 2. Set Up Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test the Bot
```bash
python test_bot.py
```

### 5. Run Locally (Optional)
```bash
python twitter_bot.py
```

## GitHub Actions Setup

### 1. Add Repository Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET` 
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `UNSPLASH_ACCESS_KEY` (optional)

### 2. Enable GitHub Actions
The workflow will automatically run every 2 hours. You can also trigger it manually from the Actions tab.

## Twitter API Setup

### 1. Apply for Twitter Developer Account
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Apply for a developer account
3. Create a new app

### 2. Get API Credentials
You'll need:
- API Key
- API Secret
- Access Token
- Access Token Secret
- Bearer Token

### 3. Set App Permissions
Make sure your app has:
- Read and Write permissions
- Tweet creation enabled

## Unsplash API Setup (Optional)

### 1. Get Unsplash API Key
1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Create a new application
3. Get your access key

### 2. Add to Environment
Add `UNSPLASH_ACCESS_KEY` to your `.env` file and GitHub secrets.

## Monitoring

### 1. Check Logs
- Local: `logs/twitter_bot_YYYYMMDD.log`
- GitHub Actions: Check the Actions tab

### 2. Monitor Twitter Account
- Check your Twitter account for posted tweets
- Monitor engagement and responses

### 3. Rate Limits
The bot handles Twitter API rate limits automatically. If you hit limits, it will wait and retry.

## Customization

### 1. Change Posting Frequency
Edit `.github/workflows/twitter_bot.yml`:
```yaml
schedule:
  - cron: '0 */4 * * *'  # Every 4 hours instead of 2
```

### 2. Add New Content Sources
Edit `twitter_bot.py` and add new scraping methods.

### 3. Modify Tweet Templates
Edit the `professional_templates` and `company_insights` lists in `twitter_bot.py`.

### 4. Change Image Probability
Edit the `include_image` probability in `run_scheduled_posts()` method.

## Troubleshooting

### Common Issues

1. **API Credentials Error**
   - Check that all Twitter API credentials are set
   - Verify credentials are correct

2. **Rate Limit Exceeded**
   - Bot handles this automatically
   - Wait for reset time

3. **Content Scraping Fails**
   - Check internet connection
   - Some sources may be temporarily unavailable

4. **Image Download Fails**
   - Check Unsplash API key
   - Images are optional, bot will post text-only

### Debug Mode
Run with debug logging:
```bash
LOG_LEVEL=DEBUG python twitter_bot.py
```

## Security Best Practices

1. **Never commit API keys**
   - Use `.env` file locally
   - Use GitHub Secrets for Actions

2. **Rotate API keys regularly**
   - Change Twitter API keys periodically

3. **Monitor bot activity**
   - Check logs regularly
   - Monitor Twitter account

## Performance Optimization

1. **Content Caching**
   - Bot scrapes fresh content each time
   - Consider caching for better performance

2. **Image Optimization**
   - Images are automatically resized for Twitter
   - Quality is optimized for file size

3. **Error Handling**
   - Bot continues running even if individual posts fail
   - Comprehensive error logging

## Legal Compliance

1. **Content Attribution**
   - All scraped content is properly attributed
   - Sources are mentioned in tweets

2. **Image Rights**
   - Uses free-to-use images from Unsplash
   - Proper attribution included

3. **Twitter Terms**
   - Bot follows Twitter's automation rules
   - Human-like posting patterns

## Support

If you encounter issues:
1. Check the logs first
2. Run the test script: `python test_bot.py`
3. Verify all environment variables are set
4. Check Twitter API status

## Updates

To update the bot:
1. Pull latest changes: `git pull`
2. Update dependencies: `pip install -r requirements.txt`
3. Test: `python test_bot.py`
4. Deploy: Push to GitHub (Actions will run automatically)
