from django.db import models
from django.utils import timezone

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('ict', 'ICT'),
        ('solar', 'Solar & Power'),
        ('general', 'General'),
    ]
    
    SOURCE_CHOICES = [
        ('news24', 'News24'),
        ('mybroadband', 'MyBroadband'),
        ('manual', 'Manual Entry'),
    ]
    
    title = models.CharField(max_length=300)
    summary = models.TextField()
    url = models.URLField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    published_date = models.DateTimeField()
    scraped_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_date']
        unique_together = ['title', 'source']
    
    def __str__(self):
        return f"{self.title} ({self.source})"
    
    def time_since_published(self):
        now = timezone.now()
        diff = now - self.published_date
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
