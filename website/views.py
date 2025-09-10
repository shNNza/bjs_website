from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import NewsArticle
import json


def index(request):
    """Render the main homepage"""
    return render(request, 'website/index.html')


def contact(request):
    """Handle contact form submission and render contact page"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        service = request.POST.get('service', '')
        message = request.POST.get('message', '')
        
        # Basic validation
        if not all([first_name, last_name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'website/contact.html')
        
        # Here you would typically save to database or send email
        # For now, we'll just show a success message
        
        messages.success(
            request, 
            f'Thank you {first_name}! Your message has been received. '
            f'We\'ll contact you at {email} soon.'
        )
        
        # Stay on contact page with success message
        return render(request, 'website/contact.html')
    
    # If GET request, render contact page
    return render(request, 'website/contact.html')


def gallery(request):
    """Render the gallery page"""
    return render(request, 'website/gallery.html')


def news(request):
    """Render the news page with scraped articles"""
    # Get ICT news articles
    ict_articles = NewsArticle.objects.filter(
        category='ict', 
        is_active=True
    ).order_by('-published_date')[:10]
    
    # Get solar/power articles if any
    solar_articles = NewsArticle.objects.filter(
        category='solar', 
        is_active=True
    ).order_by('-published_date')[:10]
    
    context = {
        'ict_articles': ict_articles,
        'solar_articles': solar_articles,
    }
    
    return render(request, 'website/news.html', context)


def team(request):
    """Render the team page"""
    return render(request, 'website/team.html')
