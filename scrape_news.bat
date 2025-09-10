@echo off
cd /d "C:\Users\Kyle Whitfield\Documents\development\bjs_website"
call .venv\Scripts\activate.bat
python manage.py scrape_news
echo News scraping completed at %date% %time% >> scrape_news.log