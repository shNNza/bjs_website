from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json


def index(request):
    """Render the main homepage"""
    return render(request, 'website/index.html')


def contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        service = request.POST.get('service', '')
        message = request.POST.get('message', '')
        
        # Basic validation
        if not all([first_name, last_name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'website/index.html')
        
        # Here you would typically save to database or send email
        # For now, we'll just show a success message
        
        messages.success(
            request, 
            f'Thank you {first_name}! Your message has been received. '
            f'We\'ll contact you at {email} soon.'
        )
        
        # Redirect back to homepage with success message
        return render(request, 'website/index.html')
    
    # If GET request, redirect to homepage
    return render(request, 'website/index.html')
