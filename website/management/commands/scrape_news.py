import requests
import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from bs4 import BeautifulSoup
from website.models import NewsArticle

class Command(BaseCommand):
    help = 'Scrape IT news from News24 and MyBroadband'

    # Keywords to categorize articles
    POWER_SOLAR_KEYWORDS = [
        'solar', 'power', 'energy', 'eskom', 'electric', 'electricity', 'battery', 'batteries',
        'ups', 'generator', 'renewable', 'grid', 'load shedding', 'loadshedding', 'outage',
        'voltage', 'watt', 'kwh', 'solar panel', 'inverter', 'backup power', 'power supply',
        'electrical', 'hydro', 'wind power', 'coal', 'nuclear power', 'utility', 'power grid'
    ]
    
    ICT_KEYWORDS = [
        'technology', 'tech', 'software', 'hardware', 'computer', 'laptop', 'server', 'network',
        'internet', 'cyber', 'digital', 'programming', 'coding', 'app', 'mobile', 'smartphone',
        'ai', 'artificial intelligence', 'machine learning', 'cloud', 'data', 'security',
        'blockchain', 'cryptocurrency', 'bitcoin', 'fintech', 'startup', 'innovation',
        'telecommunications', 'telecom', 'fiber', 'broadband', '5g', '4g', 'wireless'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-articles',
            type=int,
            default=10,
            help='Maximum number of articles to scrape per source',
        )
    
    def categorize_article(self, title, summary):
        """Determine article category based on title and summary content"""
        text = (title + ' ' + summary).lower()
        
        # Count matches for each category
        power_matches = sum(1 for keyword in self.POWER_SOLAR_KEYWORDS if keyword in text)
        ict_matches = sum(1 for keyword in self.ICT_KEYWORDS if keyword in text)
        
        # Prioritize power/solar if there are matches (since ICT sites often cover energy news)
        if power_matches > 0:
            return 'solar'
        elif ict_matches > 0:
            return 'ict'
        else:
            # Default to ICT for tech sites, but could be refined
            return 'ict'

    def handle(self, *args, **options):
        max_articles = options['max_articles']
        
        self.stdout.write(self.style.SUCCESS('Starting news scraping...'))
        
        # Scrape News24
        news24_count = self.scrape_news24(max_articles)
        
        # Scrape MyBroadband
        mybroadband_count = self.scrape_mybroadband(max_articles)
        
        # Clean up old articles (older than 30 days)
        self.cleanup_old_articles()
        
        # Show category breakdown
        ict_total = NewsArticle.objects.filter(category='ict', is_active=True).count()
        solar_total = NewsArticle.objects.filter(category='solar', is_active=True).count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'News scraping completed successfully!\n'
                f'News24 articles: {news24_count}\n'
                f'MyBroadband articles: {mybroadband_count}\n'
                f'Total new articles: {news24_count + mybroadband_count}\n'
                f'\nCurrent database totals:\n'
                f'ICT News: {ict_total} articles\n'
                f'Solar & Power News: {solar_total} articles'
            )
        )

    def scrape_news24(self, max_articles):
        """Scrape IT-related news from News24"""
        count = 0
        try:
            # Search for IT/technology related news on News24
            url = "https://www.news24.com/tags/topics/it"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links and titles
            articles = soup.find_all('article', class_=lambda x: x and 'article' in x.lower())[:max_articles]
            
            for article in articles:
                try:
                    title_elem = article.find(['h1', 'h2', 'h3'], class_=lambda x: x and 'title' in x.lower())
                    if not title_elem:
                        title_elem = article.find('a')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                        
                        if link_elem and link_elem.get('href'):
                            url = link_elem['href']
                            if not url.startswith('http'):
                                url = 'https://www.news24.com' + url
                            
                            # Get article summary
                            summary_elem = article.find('p', class_=lambda x: x and ('summary' in x.lower() or 'excerpt' in x.lower()))
                            if not summary_elem:
                                summary_elem = article.find('p')
                            
                            summary = summary_elem.get_text(strip=True)[:500] if summary_elem else title[:200] + "..."
                            
                            # Determine category based on content
                            category = self.categorize_article(title, summary)
                            
                            # Check if article already exists
                            if not NewsArticle.objects.filter(title=title, source='news24').exists():
                                NewsArticle.objects.create(
                                    title=title,
                                    summary=summary,
                                    url=url,
                                    source='news24',
                                    category=category,
                                    published_date=timezone.now(),
                                )
                                count += 1
                                self.stdout.write(f'  Added News24 article ({category}): {title[:50]}...')
                                
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error processing News24 article: {e}'))
                    continue
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scraping News24: {e}'))
            
        return count

    def scrape_mybroadband(self, max_articles):
        """Scrape IT news from MyBroadband"""
        count = 0
        try:
            # MyBroadband main page
            url = "https://mybroadband.co.za/news"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and ('post' in x.lower() or 'article' in x.lower()))[:max_articles]
            
            for article in articles:
                try:
                    title_elem = article.find(['h1', 'h2', 'h3'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        
                        # Find the link
                        link_elem = title_elem.find('a') or article.find('a')
                        if link_elem and link_elem.get('href'):
                            url = link_elem['href']
                            if not url.startswith('http'):
                                url = 'https://mybroadband.co.za' + url
                            
                            # Get summary
                            summary_elem = article.find('p', class_=lambda x: x and ('excerpt' in x.lower() or 'summary' in x.lower()))
                            if not summary_elem:
                                summary_elem = article.find('p')
                            
                            summary = summary_elem.get_text(strip=True)[:500] if summary_elem else title[:200] + "..."
                            
                            # Determine category based on content
                            category = self.categorize_article(title, summary)
                            
                            # Check if article already exists
                            if not NewsArticle.objects.filter(title=title, source='mybroadband').exists():
                                NewsArticle.objects.create(
                                    title=title,
                                    summary=summary,
                                    url=url,
                                    source='mybroadband',
                                    category=category,
                                    published_date=timezone.now(),
                                )
                                count += 1
                                self.stdout.write(f'  Added MyBroadband article ({category}): {title[:50]}...')
                                
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error processing MyBroadband article: {e}'))
                    continue
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scraping MyBroadband: {e}'))
            
        return count

    def cleanup_old_articles(self):
        """Remove articles older than 30 days"""
        cutoff_date = timezone.now() - timedelta(days=30)
        old_articles = NewsArticle.objects.filter(scraped_date__lt=cutoff_date)
        count = old_articles.count()
        old_articles.delete()
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Cleaned up {count} old articles'))