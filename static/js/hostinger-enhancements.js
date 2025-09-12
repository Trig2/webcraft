// Hostinger-inspired Interactive Enhancements
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth color transitions for interactive elements
    function addHostingerInteractivity() {
        // Enhanced button hover effects
        const buttons = document.querySelectorAll('.hostinger-btn-primary, .hostinger-btn-secondary, .hostinger-btn-outline');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.02)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Card hover animations
        const cards = document.querySelectorAll('.hostinger-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px)';
                this.style.boxShadow = '0 25px 50px -12px rgba(147, 51, 234, 0.25)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
            });
        });

        // Social icon enhanced effects
        const socialIcons = document.querySelectorAll('.hostinger-social-icon');
        socialIcons.forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) rotate(5deg) scale(1.1)';
                this.style.boxShadow = '0 12px 20px rgba(147, 51, 234, 0.4)';
            });
            
            icon.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) rotate(0deg) scale(1)';
                this.style.boxShadow = '0 4px 12px rgba(168, 85, 247, 0.3)';
            });
        });
    }

    // Dynamic gradient background animation
    function initDynamicBackground() {
        const hero = document.querySelector('.hostinger-section-light');
        if (hero) {
            let mouseX = 0;
            let mouseY = 0;
            
            hero.addEventListener('mousemove', function(e) {
                const rect = hero.getBoundingClientRect();
                mouseX = ((e.clientX - rect.left) / rect.width) * 100;
                mouseY = ((e.clientY - rect.top) / rect.height) * 100;
                
                hero.style.background = `radial-gradient(circle at ${mouseX}% ${mouseY}%, 
                    rgba(168, 85, 247, 0.1) 0%, 
                    rgba(249, 115, 22, 0.05) 25%, 
                    rgba(168, 85, 247, 0.03) 50%, 
                    transparent 70%), 
                    linear-gradient(135deg, var(--neutral-50) 0%, var(--primary-50) 100%)`;
            });
        }
    }

    // Scroll-triggered color animations
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('hostinger-fade-in', 'visible');
                    
                    // Add staggered animation for card grids
                    if (entry.target.classList.contains('hostinger-card-grid')) {
                        const cards = entry.target.querySelectorAll('.hostinger-card');
                        cards.forEach((card, index) => {
                            setTimeout(() => {
                                card.style.opacity = '1';
                                card.style.transform = 'translateY(0)';
                            }, index * 100);
                        });
                    }
                }
            });
        }, observerOptions);

        // Observe elements for animations
        const animatedElements = document.querySelectorAll('.hostinger-card, .hostinger-card-grid, [data-aos]');
        animatedElements.forEach(el => {
            el.classList.add('hostinger-fade-in');
            observer.observe(el);
        });
    }

    // Color theme toggle functionality (optional)
    function initThemeToggle() {
        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '<i class="fas fa-palette"></i>';
        toggleButton.className = 'fixed bottom-20 right-6 z-50 w-12 h-12 rounded-full bg-white shadow-lg border-2 border-purple-200 text-purple-600 hover:bg-purple-50 transition-all duration-300';
        toggleButton.title = 'Toggle Color Theme';
        
        let currentTheme = 'default';
        const themes = {
            default: {
                '--primary-600': '#9333ea',
                '--secondary-500': '#f97316'
            },
            blue: {
                '--primary-600': '#2563eb',
                '--secondary-500': '#06b6d4'
            },
            green: {
                '--primary-600': '#059669',
                '--secondary-500': '#84cc16'
            }
        };

        toggleButton.addEventListener('click', function() {
            const themeKeys = Object.keys(themes);
            const currentIndex = themeKeys.indexOf(currentTheme);
            const nextIndex = (currentIndex + 1) % themeKeys.length;
            currentTheme = themeKeys[nextIndex];
            
            const theme = themes[currentTheme];
            Object.entries(theme).forEach(([property, value]) => {
                document.documentElement.style.setProperty(property, value);
            });
            
            // Add visual feedback
            toggleButton.style.transform = 'scale(0.9)';
            setTimeout(() => {
                toggleButton.style.transform = 'scale(1)';
            }, 150);
        });

        document.body.appendChild(toggleButton);
    }

    // Floating particle effect for newsletter section
    function initFloatingParticles() {
        const newsletter = document.querySelector('.hostinger-newsletter');
        if (newsletter) {
            for (let i = 0; i < 5; i++) {
                const particle = document.createElement('div');
                particle.className = 'absolute w-2 h-2 bg-white rounded-full opacity-20 animate-pulse';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 3 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
                newsletter.appendChild(particle);
                
                // Animate particle movement
                setInterval(() => {
                    particle.style.transform = `translate(${Math.random() * 20 - 10}px, ${Math.random() * 20 - 10}px)`;
                }, 2000);
            }
        }
    }

    // Form enhancement with Hostinger colors
    function enhanceForms() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (!input.classList.contains('hostinger-input') && !input.classList.contains('hostinger-textarea')) {
                input.classList.add('hostinger-input');
            }
            
            // Add focus ring effect
            input.addEventListener('focus', function() {
                this.style.borderColor = 'var(--primary-500)';
                this.style.boxShadow = '0 0 0 3px rgba(168, 85, 247, 0.1)';
            });
            
            input.addEventListener('blur', function() {
                this.style.borderColor = 'var(--neutral-200)';
                this.style.boxShadow = 'none';
            });
        });
    }

    // Initialize all enhancements
    addHostingerInteractivity();
    initDynamicBackground();
    initScrollAnimations();
    initThemeToggle();
    initFloatingParticles();
    enhanceForms();

    // Add loading complete animation
    setTimeout(() => {
        document.body.classList.add('hostinger-loaded');
    }, 100);
});

// CSS Animation classes that will be added dynamically
const style = document.createElement('style');
style.textContent = `
    .hostinger-loaded {
        opacity: 1;
        transition: opacity 0.5s ease;
    }
    
    .hostinger-loaded .hostinger-fade-in.visible {
        animation: hostingerSlideIn 0.6s ease forwards;
    }
    
    @keyframes hostingerSlideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hostinger-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .hostinger-social-icon {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .hostinger-btn-primary,
    .hostinger-btn-secondary,
    .hostinger-btn-outline {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .hostinger-btn-primary::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .hostinger-btn-primary:hover::before {
        left: 100%;
    }
`;
document.head.appendChild(style);
