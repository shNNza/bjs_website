document.addEventListener('DOMContentLoaded', function() {
    // ANIMATED COUNTER FUNCTION FOR BOUNCING BLOCKS
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 60;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
                
                // Add suffix based on the stat
                if (target === 20) {
                    element.textContent = current + '+';
                } else if (target === 500) {
                    element.textContent = current + '+';
                } else if (target === 24) {
                    element.textContent = '24/7';
                } else if (target === 100) {
                    element.textContent = current + '%';
                }
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }

    // Intersection Observer for BOUNCING STATS Animation
    const bounceStatsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const countNumbers = entry.target.querySelectorAll('.count-number');
                countNumbers.forEach(stat => {
                    if (!stat.classList.contains('animated')) {
                        stat.classList.add('animated', 'animating');
                        const target = parseInt(stat.getAttribute('data-target'));
                        animateCounter(stat, target);
                    }
                });
            }
        });
    }, { threshold: 0.3 });

    // Observe the BOUNCING stats section
    const bounceStatsSection = document.querySelector('.stats-container');
    if (bounceStatsSection) {
        bounceStatsObserver.observe(bounceStatsSection);
    }

    // Contact Form Handling
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(contactForm);
            const data = {
                firstName: formData.get('firstName'),
                lastName: formData.get('lastName'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                service: formData.get('service'),
                message: formData.get('message')
            };
            
            // Basic validation
            if (!data.firstName || !data.lastName || !data.email || !data.message) {
                showFormMessage('Please fill in all required fields.', 'error');
                return;
            }
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(data.email)) {
                showFormMessage('Please enter a valid email address.', 'error');
                return;
            }
            
            // Simulate form submission (replace with actual backend call)
            submitContactForm(data);
        });
    }

    function submitContactForm(data) {
        // Change button text
        const submitBtn = document.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        // Simulate API call delay
        setTimeout(() => {
            // For demonstration - show success message
            showFormMessage('Thank you! Your message has been received. We\'ll contact you at ' + data.email + ' soon.', 'success');
            contactForm.reset();
            
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    }

    function showFormMessage(message, type) {
        formMessage.textContent = message;
        formMessage.className = 'form-message ' + type;
        formMessage.style.display = 'block';
        
        // Hide message after 5 seconds
        setTimeout(() => {
            formMessage.style.display = 'none';
        }, 5000);
    }

    // Slideshow functionality
    const slides = document.querySelectorAll('.slide');
    const navDots = document.querySelectorAll('.nav-dot');
    let currentSlide = 0;
    let slideInterval;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        navDots.forEach(dot => dot.classList.remove('active'));
        
        slides[index].classList.add('active');
        navDots[index].classList.add('active');
        
        currentSlide = index;
    }

    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }

    function startSlideshow() {
        slideInterval = setInterval(nextSlide, 6000);
    }

    function stopSlideshow() {
        clearInterval(slideInterval);
    }

    navDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopSlideshow();
            showSlide(index);
            startSlideshow();
        });
    });

    startSlideshow();

    const heroSection = document.querySelector('.hero');
    heroSection.addEventListener('mouseenter', stopSlideshow);
    heroSection.addEventListener('mouseleave', startSlideshow);

    // Navigation scroll behavior
    let lastScrollTop = 0;
    const navbar = document.getElementById('navbar');
    const contactBar = document.getElementById('contactBar');
    
    if (navbar && contactBar) {
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.classList.add('hidden');
                contactBar.classList.add('hidden');
            } else {
                navbar.classList.remove('hidden');
                contactBar.classList.remove('hidden');
            }
            
            lastScrollTop = scrollTop;
        });
    }

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        if (el) {
            observer.observe(el);
        }
    });
});