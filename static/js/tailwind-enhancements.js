// Tailwind Enhancements for Landing Page
document.addEventListener('DOMContentLoaded', function() {
    // Apply hero section enhancements
    const heroSection = document.querySelector('section:first-of-type');
    if (heroSection) {
        heroSection.classList.add('hero-section');
        
        // Find hero content
        const heroContent = heroSection.querySelector('.md\\:w-1\\/2:first-of-type');
        if (heroContent) {
            heroContent.classList.add('hero-content', 'rounded-xl');
        }
        
        // Find hero image container
        const heroImageContainer = heroSection.querySelector('.md\\:w-1\\/2:last-of-type');
        if (heroImageContainer) {
            heroImageContainer.classList.add('hero-image-container');
            heroImageContainer.classList.remove('animate-bounce');
            
            // Find hero image
            const heroImage = heroImageContainer.querySelector('img');
            if (heroImage) {
                heroImage.classList.add('hero-image', 'animate-float');
            }
        }
        
        // Find trust indicators
        const trustIndicators = heroSection.querySelector('.mt-12');
        if (trustIndicators) {
            trustIndicators.classList.add('trust-indicators');
            trustIndicators.classList.remove('mt-12');
            trustIndicators.classList.add('mt-8');
            
            // Find indicators
            const indicators = trustIndicators.querySelectorAll('.flex.items-center');
            indicators.forEach(indicator => {
                indicator.classList.add('indicator');
            });
        }
    }
    
    // Apply service card enhancements
    const serviceCards = document.querySelectorAll('.card');
    serviceCards.forEach(card => {
        card.classList.add('service-card');
        
        // Find service icon
        const serviceIcon = card.querySelector('.w-16.h-16');
        if (serviceIcon) {
            serviceIcon.classList.add('service-icon');
        }
    });
    
    // Apply testimonial card enhancements
    const testimonialSection = document.querySelector('section:nth-of-type(3)');
    if (testimonialSection) {
        const testimonialCards = testimonialSection.querySelectorAll('.bg-white.rounded-lg');
        testimonialCards.forEach(card => {
            card.classList.add('testimonial-card');
        });
    }
    
    // Apply CTA section enhancements
    const ctaSection = document.querySelector('section.py-20.text-white');
    if (ctaSection) {
        ctaSection.classList.add('cta-section');
        
        // Find CTA content
        const ctaContent = ctaSection.querySelector('.container');
        if (ctaContent) {
            ctaContent.classList.add('cta-content');
        }
    }
    
    // Apply feature card enhancements
    const featureSection = document.querySelector('section.py-20.bg-white');
    if (featureSection) {
        const featureCards = featureSection.querySelectorAll('.text-center.p-8');
        featureCards.forEach(card => {
            card.classList.add('feature-card');
            
            // Find feature icon
            const featureIcon = card.querySelector('.text-blue-600');
            if (featureIcon) {
                featureIcon.classList.add('feature-icon');
            }
        });
    }
    
    // Apply button enhancements
    const primaryButtons = document.querySelectorAll('.btn-primary');
    primaryButtons.forEach(button => {
        if (!button.classList.contains('px-6')) {
            button.classList.add('px-6', 'py-3', 'rounded-lg', 'text-white', 'font-semibold');
        }
    });
    
    const secondaryButtons = document.querySelectorAll('.btn-secondary');
    secondaryButtons.forEach(button => {
        if (!button.classList.contains('px-6')) {
            button.classList.add('px-6', 'py-3', 'rounded-lg', 'font-semibold');
        }
    });
    
    // Apply animation utilities
    const animateElements = document.querySelectorAll('.hover-scale, .hover-rotate');
    animateElements.forEach(element => {
        if (element.classList.contains('hover-scale')) {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        }
        
        if (element.classList.contains('hover-rotate')) {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'rotate(5deg)';
            });
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'rotate(0)';
            });
        }
    });
});