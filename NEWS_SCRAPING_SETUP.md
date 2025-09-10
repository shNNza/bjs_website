# News Scraping Setup Guide

## Overview
This system automatically scrapes IT-related news from News24 and MyBroadband every 24 hours and displays them on the news page.

## Components
1. **NewsArticle Model**: Stores scraped news articles with title, summary, URL, source, category, and timestamps
2. **Management Command**: `scrape_news` command that performs the actual scraping
3. **Automated Scheduling**: Windows Task Scheduler integration for 24-hour refresh
4. **Dynamic News Display**: Updated news page template showing live scraped content

## Manual News Scraping
To manually scrape news, run:
```bash
python manage.py scrape_news
```

Options:
- `--max-articles=N`: Limit number of articles per source (default: 10)

## Setting Up Automated 24-Hour Refresh

### Method 1: Windows Task Scheduler (Recommended)
1. Open Task Scheduler (`taskschd.msc`)
2. Click "Create Basic Task"
3. Name: "Blue Joy Solutions - News Scraping"
4. Trigger: Daily, at your preferred time (e.g., 6:00 AM)
5. Action: "Start a program"
6. Program/script: `C:\Users\Kyle Whitfield\Documents\development\bjs_website\scrape_news.bat`
7. Start in: `C:\Users\Kyle Whitfield\Documents\development\bjs_website`

### Method 2: Python-based Scheduling (Alternative)
If you prefer Python-based scheduling, install `schedule` package:
```bash
pip install schedule
```

Then create a scheduler service (requires additional setup).

## Current Status
- ✅ MyBroadband scraping: Working (successfully scraped articles)
- ❌ News24 scraping: Blocked (403 Forbidden error)
- ✅ Database storage: Working
- ✅ News page display: Working

## Troubleshooting

### News24 Access Issues
News24 blocks automated requests. Potential solutions:
1. Use RSS feeds instead of web scraping
2. Implement rotating user agents and request delays
3. Use proxy rotation
4. Contact News24 for API access

### No Articles Showing
1. Check if scraping command ran successfully
2. Verify database has articles: Check Django admin or database directly
3. Ensure articles are marked as `is_active=True`

### Scraping Failures
- Check internet connection
- Verify target website structure hasn't changed
- Check scraping logs for error details

## Files Created
- `website/models.py`: NewsArticle model
- `website/management/commands/scrape_news.py`: Scraping command
- `website/views.py`: Updated news view
- `website/templates/website/news.html`: Updated template
- `scrape_news.bat`: Windows batch script for scheduling
- `scrape_news.log`: Log file (created when batch runs)

## Database Maintenance
- Articles older than 30 days are automatically cleaned up
- Duplicate articles (same title + source) are prevented
- Articles can be manually managed via Django admin

## Next Steps
1. Set up Windows Task Scheduler using the batch file
2. Monitor scraping logs for any issues
3. Consider adding more news sources
4. Implement RSS feed integration for more reliable data