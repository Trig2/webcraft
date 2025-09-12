from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import ChatMessage
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populate chat models with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--messages',
            type=int,
            default=100,
            help='Number of chat messages to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Chat Data Population...'))
        
        self.create_chat_messages(options['messages'])
        
        self.stdout.write(self.style.SUCCESS('✅ Chat data population completed!'))

    def create_chat_messages(self, count):
        self.stdout.write(f'Creating {count} chat messages...')
        
        users = list(User.objects.all())
        
        # Sample chat messages for different scenarios
        messages = [
            "Hello! I'm interested in your web development services.",
            "Can you tell me more about your pricing plans?",
            "I need a website for my small business. What do you recommend?",
            "How long does it typically take to complete a project?",
            "Do you offer e-commerce solutions?",
            "I'd like to schedule a consultation call.",
            "What technologies do you work with?",
            "Can you help with website maintenance?",
            "I'm looking for a complete digital marketing solution.",
            "Do you provide SEO services as well?",
            "What's included in your basic web package?",
            "I have a WordPress site that needs updating.",
            "Can you help migrate my site to a new platform?",
            "I need a mobile app along with the website.",
            "What's your process for custom development?",
            "Do you work with clients internationally?",
            "I'd like to see some examples of your recent work.",
            "What kind of support do you provide after launch?",
            "Can you integrate payment gateways?",
            "I need help with website security.",
            "Do you offer hosting services?",
            "What's the difference between your packages?",
            "Can you help with logo design as well?",
            "I need a website that works well on mobile.",
            "How do you handle project revisions?",
            "What's your policy on project deadlines?",
            "Can you work within my budget constraints?",
            "I need help with email marketing integration.",
            "Do you provide training on how to use the CMS?",
            "Can you help optimize my site for search engines?",
            "I'm having issues with my current website.",
            "What happens if I need changes after the site goes live?",
            "Do you offer monthly maintenance packages?",
            "Can you help with social media integration?",
            "I need analytics and tracking set up.",
            "What's the best platform for my type of business?",
            "Can you help with content creation?",
            "I need help with online store setup.",
            "Do you provide backup and recovery services?",
            "Can you help improve my site's loading speed?",
            "What's included in your consultation?",
            "I need help with multi-language support.",
            "Can you integrate with my existing systems?",
            "What kind of documentation do you provide?",
            "I need help with user authentication features.",
            "Can you set up automated workflows?",
            "What's your experience with my industry?",
            "Do you provide performance monitoring?",
            "Can you help with accessibility compliance?",
            "I need help with database optimization."
        ]
        
        # Admin/Support responses
        support_responses = [
            "Thank you for your interest! I'd be happy to help you with that.",
            "Let me connect you with one of our specialists who can provide detailed information.",
            "That's a great question! Our team has extensive experience in that area.",
            "I'll send you some examples of similar projects we've completed.",
            "We offer flexible pricing options to fit different budgets.",
            "Let's schedule a call to discuss your specific requirements.",
            "Our typical project timeline is 2-4 weeks depending on complexity.",
            "We provide comprehensive support throughout the entire process.",
            "I can send you our detailed service brochure with all the information.",
            "That's definitely something we can help you with.",
            "Our team specializes in creating custom solutions for businesses like yours.",
            "We include SEO optimization in all our web development packages.",
            "I'll have our project manager reach out to discuss the details.",
            "We work with clients worldwide and have experience in various industries.",
            "Our packages include ongoing maintenance and support options.",
            "Let me check our current availability and get back to you.",
            "We use the latest technologies to ensure your site performs optimally.",
            "I'll send you a custom quote based on your specific needs.",
            "Our team can definitely integrate with your existing systems.",
            "We provide detailed documentation and training for all our solutions."
        ]
        
        # Create chat messages with realistic conversation flow
        for i in range(count):
            user = random.choice(users)
            
            # 70% chance of user messages, 30% chance of support responses
            if random.random() < 0.7:
                message = random.choice(messages)
                # Use non-staff users for customer messages
                user = random.choice([u for u in users if not u.is_staff]) if any(not u.is_staff for u in users) else user
            else:
                message = random.choice(support_responses)
                # Use staff users for support responses
                user = random.choice([u for u in users if u.is_staff]) if any(u.is_staff for u in users) else user
            
            ChatMessage.objects.create(
                user=user,
                message=message
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} chat messages'))
