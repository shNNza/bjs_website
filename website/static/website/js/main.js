// Loading Animation
function hideLoadingOverlay() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('fade-out');
        setTimeout(() => {
            loadingOverlay.style.display = 'none';
            // Remember that loading has been completed
            sessionStorage.setItem('loadingCompleted', 'true');
        }, 500);
    }
}

// Check if loading should be shown (only for first visit in session)
function initializeLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingCompleted = sessionStorage.getItem('loadingCompleted');
    
    if (loadingCompleted && loadingOverlay) {
        // Skip loading animation for subsequent page visits
        loadingOverlay.style.display = 'none';
    }
}

// Initialize loading on page load
initializeLoading();

// Show loading overlay immediately
document.addEventListener('DOMContentLoaded', function() {
    // Hide loading overlay when page is fully loaded
    window.addEventListener('load', function() {
        // Add small delay to ensure smooth transition
        setTimeout(hideLoadingOverlay, 200);
    });

    // Fallback: Hide loading overlay after maximum 5 seconds
    setTimeout(() => {
        hideLoadingOverlay();
    }, 5000);

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

    // Intersection Observer for BOUNCING STATS Animation with restart capability
    const bounceStatsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statBlocks = entry.target.querySelectorAll('.bounce-stat-block');
                const countNumbers = entry.target.querySelectorAll('.count-number');
                
                // Fade in blocks from the right only on first view (if not already faded in)
                statBlocks.forEach((block, index) => {
                    if (!block.classList.contains('fade-in-right')) {
                        setTimeout(() => {
                            block.classList.add('fade-in-right');
                        }, index * 150); // Stagger by 150ms
                    }
                });

                // Always restart counter animations when section comes into view
                countNumbers.forEach(stat => {
                    // Reset counter to 0 and remove animated class to allow restart
                    stat.textContent = '0';
                    stat.classList.remove('animated');
                    
                    // Start counter animation (with delay only if blocks haven't faded in yet)
                    const hasNotFadedIn = !statBlocks[0].classList.contains('fade-in-right');
                    const delay = hasNotFadedIn ? 400 : 0; // Delay only for first time
                    
                    setTimeout(() => {
                        stat.classList.add('animated', 'animating');
                        const target = parseInt(stat.getAttribute('data-target'));
                        animateCounter(stat, target);
                    }, delay);
                });
            } else {
                // Only reset counter animations when out of view, keep fade-in state
                const countNumbers = entry.target.querySelectorAll('.count-number');
                
                countNumbers.forEach(stat => {
                    stat.classList.remove('animated', 'animating');
                    stat.textContent = '0';
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
        slideInterval = setInterval(nextSlide, 8000); // 8 seconds to allow time to see the zoom animation
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

    // Only initialize slideshow if hero section exists (home page)
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        startSlideshow();
        heroSection.addEventListener('mouseenter', stopSlideshow);
        heroSection.addEventListener('mouseleave', startSlideshow);
    }

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
            } else if (scrollTop < lastScrollTop) {
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

    // Gallery functionality
    if (document.querySelector('.gallery-grid')) {
        initGallery();
    }

    // News functionality
    if (document.querySelector('.news-grid')) {
        initNews();
    }

    // Circuit board divider scroll animation
    initCircuitAnimation();

    // Cookie Consent functionality (same as home page)
    initializeCookieConsent();
});

// Gallery Functions
function initGallery() {
    // Filter functionality
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            
            const filterValue = btn.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease-in-out';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Modal functionality
    const modal = document.getElementById('mediaModal');
    const modalImage = document.getElementById('modalImage');
    const modalVideo = document.getElementById('modalVideo');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalClose = document.querySelector('.modal-close');
    
    // View buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            
            const src = btn.getAttribute('data-src');
            const type = btn.getAttribute('data-type');
            const title = btn.parentElement.querySelector('h3').textContent;
            const description = btn.parentElement.querySelector('p').textContent;
            
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            
            if (type === 'image') {
                modalImage.src = src;
                modalImage.style.display = 'block';
                modalVideo.style.display = 'none';
            } else if (type === 'video') {
                modalVideo.querySelector('source').src = src;
                modalVideo.load();
                modalVideo.style.display = 'block';
                modalImage.style.display = 'none';
            }
            
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Gallery items click
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', () => {
            const viewBtn = item.querySelector('.view-btn');
            if (viewBtn) {
                viewBtn.click();
            }
        });
    });
    
    // Close modal
    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
    
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Pause video if playing
        if (modalVideo.style.display === 'block') {
            modalVideo.pause();
            modalVideo.currentTime = 0;
        }
    }
}

// Add fadeIn animation keyframes via CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// News Functions
function initNews() {
    // Filter functionality
    const filterBtns = document.querySelectorAll('.news-filter-btn');
    const newsItems = document.querySelectorAll('.news-item');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            
            const filterValue = btn.getAttribute('data-filter');
            
            newsItems.forEach(item => {
                const category = item.getAttribute('data-category');
                if (filterValue === 'all' || category === filterValue) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease-in-out';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Initialize news feeds (placeholder - will be enhanced with real API calls)
    loadNewsFeeds();
}

// Placeholder function for loading news feeds
// In production, this would make API calls to Facebook, News24, etc.
function loadNewsFeeds() {
    console.log('News feeds initialized. Ready for API integration.');
    
    // Facebook Graph API integration would go here
    // loadFacebookFeed();
    
    // News24 RSS/API integration would go here
    // loadNews24Feed();
    
    // Other news sources would go here
    // loadOtherNewsFeeds();
}

// Placeholder for Facebook API integration
function loadFacebookFeed() {
    // This would use Facebook Graph API to fetch posts
    // Example: https://graph.facebook.com/v18.0/{page-id}/posts?access_token={access-token}
    console.log('Facebook feed integration placeholder');
}

// Placeholder for News24 integration
function loadNews24Feed() {
    // This would fetch RSS feeds or use News24 API
    // Filter for ICT and Solar/Power related content
    console.log('News24 feed integration placeholder');
}

// Cookie Consent functionality (same as home page)
function initializeCookieConsent() {
    const cookiesButton = document.getElementById('cookiesButton');
    const cookiesPopup = document.getElementById('cookiesPopup');
    const cookiesOverlay = document.getElementById('cookiesOverlay');
    const acceptBtn = document.getElementById('acceptCookies');
    const denyBtn = document.getElementById('denyCookies');
    const preferencesBtn = document.getElementById('preferencesCookies');
    const closeBtn = document.getElementById('closeCookies');

    // Check if elements exist (they may not exist on all pages yet)
    if (!cookiesButton || !cookiesPopup || !cookiesOverlay) {
        return;
    }

    // Check if cookies consent has already been given
    const cookiesConsent = localStorage.getItem('cookiesConsent');
    if (cookiesConsent) {
        cookiesButton.style.display = 'none';
    }

    // Open cookies popup
    cookiesButton.addEventListener('click', function() {
        cookiesPopup.classList.add('active');
        cookiesOverlay.classList.add('active');
    });

    // Close popup when clicking overlay
    cookiesOverlay.addEventListener('click', function() {
        cookiesPopup.classList.remove('active');
        cookiesOverlay.classList.remove('active');
    });

    // Close popup when clicking close button
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            cookiesPopup.classList.remove('active');
            cookiesOverlay.classList.remove('active');
        });
    }

    // Accept cookies
    if (acceptBtn) {
        acceptBtn.addEventListener('click', function() {
            localStorage.setItem('cookiesConsent', 'accepted');
            cookiesPopup.classList.remove('active');
            cookiesOverlay.classList.remove('active');
            cookiesButton.style.display = 'none';
            console.log('Cookies accepted');
        });
    }

    // Deny cookies
    if (denyBtn) {
        denyBtn.addEventListener('click', function() {
            localStorage.setItem('cookiesConsent', 'denied');
            cookiesPopup.classList.remove('active');
            cookiesOverlay.classList.remove('active');
            cookiesButton.style.display = 'none';
            console.log('Cookies denied');
        });
    }

    // View preferences
    if (preferencesBtn) {
        preferencesBtn.addEventListener('click', function() {
            showCookiePreferences();
        });
    }
}

// Cookie Preferences functionality (inline with cookie popup)
function showCookiePreferences() {
    const preferencesDiv = document.getElementById('cookiePreferencesSection');
    const mainButtons = document.getElementById('mainCookieButtons');
    
    if (preferencesDiv.style.display === 'none') {
        preferencesDiv.style.display = 'block';
        mainButtons.style.display = 'none';
        loadCookiePreferences();
    }
}

function hideCookiePreferences() {
    const preferencesDiv = document.getElementById('cookiePreferencesSection');
    const mainButtons = document.getElementById('mainCookieButtons');
    
    preferencesDiv.style.display = 'none';
    mainButtons.style.display = 'block';
}

function toggleCategoryExpansion(category) {
    const description = document.getElementById(category + '-description');
    const expandBtn = document.querySelector(`[onclick="toggleCategoryExpansion('${category}')"] svg`);
    
    if (description.style.display === 'none' || description.style.display === '') {
        description.style.display = 'block';
        expandBtn.style.transform = 'rotate(180deg)';
    } else {
        description.style.display = 'none';
        expandBtn.style.transform = 'rotate(0deg)';
    }
}

function loadCookiePreferences() {
    const preferences = JSON.parse(localStorage.getItem('cookiePreferences') || '{}');
    
    const statisticsCheckbox = document.getElementById('statisticsCookies');
    const marketingCheckbox = document.getElementById('marketingCookies');
    
    if (statisticsCheckbox) statisticsCheckbox.checked = preferences.statistics || false;
    if (marketingCheckbox) marketingCheckbox.checked = preferences.marketing || false;
}

function saveCookiePreferences() {
    const statisticsCheckbox = document.getElementById('statisticsCookies');
    const marketingCheckbox = document.getElementById('marketingCookies');
    
    const preferences = {
        functional: true, // Always true, required
        statistics: statisticsCheckbox ? statisticsCheckbox.checked : false,
        marketing: marketingCheckbox ? marketingCheckbox.checked : false
    };
    
    localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
    localStorage.setItem('cookiesConsent', 'customized');
    
    // Hide cookie elements
    const cookiesButton = document.getElementById('cookiesButton');
    const cookiesPopup = document.getElementById('cookiesPopup');
    const cookiesOverlay = document.getElementById('cookiesOverlay');
    
    if (cookiesButton) cookiesButton.style.display = 'none';
    if (cookiesPopup) cookiesPopup.classList.remove('active');
    if (cookiesOverlay) cookiesOverlay.classList.remove('active');
    
    console.log('Cookie preferences saved:', preferences);
}

// Circuit Board Animation Functions
function initCircuitAnimation() {
    const circuitDots = document.querySelectorAll('.circuit-moving-dot');
    
    if (circuitDots.length === 0) return; // Only run on pages with circuit dividers
    
    let lastScrollY = 0;
    let ticking = false;
    
    function updateCircuitDots() {
        const scrollY = window.pageYOffset;
        const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollProgress = Math.min(scrollY / documentHeight, 1);
        
        circuitDots.forEach((dot, index) => {
            // Each dot moves at slightly different rates for variety
            const dotProgress = (scrollProgress + (index * 0.1)) % 1;
            
            // Map scroll progress to horizontal movement (10% to 90%)
            const leftPosition = 10 + (dotProgress * 80);
            
            // Add some oscillation for more interesting movement
            const oscillation = Math.sin(scrollProgress * Math.PI * 2 + (index * Math.PI / 2)) * 5;
            
            dot.style.left = `${leftPosition + oscillation}%`;
            
            // Add glow effect when moving
            const glowIntensity = Math.abs(scrollY - lastScrollY) / 20;
            const maxGlow = Math.min(glowIntensity, 1);
            
            dot.style.boxShadow = `
                0 0 ${20 + (maxGlow * 15)}px rgba(6, 182, 212, ${0.8 + (maxGlow * 0.2)}),
                inset 0 2px 4px rgba(255, 255, 255, 0.3)
            `;
        });
        
        lastScrollY = scrollY;
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateCircuitDots);
            ticking = true;
        }
    }
    
    // Throttled scroll listener
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // Initial position
    updateCircuitDots();
}