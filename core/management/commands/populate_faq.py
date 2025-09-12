from django.core.management.base import BaseCommand
from core.models import FAQ

class Command(BaseCommand):
    help = 'Populate the FAQ table with demo data.'

    def handle(self, *args, **options):
        FAQ.objects.all().delete()
        faqs = [
            {
                "question": "What services do you offer?",
                "answer": "We offer website design, development, SEO, e-commerce, and digital marketing solutions for all business types.",
                "category": "General",
                "display_order": 1,
                "is_active": True,
            },
            {
                "question": "How long does it take to build a website?",
                "answer": "Typical projects take 2-6 weeks depending on complexity and requirements.",
                "category": "Process",
                "display_order": 2,
                "is_active": True,
            },
            {
                "question": "Do you provide support after launch?",
                "answer": "Yes, we offer ongoing support and maintenance packages to keep your site running smoothly.",
                "category": "Support",
                "display_order": 3,
                "is_active": True,
            },
            {
                "question": "Can you redesign my existing website?",
                "answer": "Absolutely! We can modernize and optimize your current website for better performance and appearance.",
                "category": "General",
                "display_order": 4,
                "is_active": True,
            },
            {
                "question": "What is your pricing structure?",
                "answer": "We offer flexible pricing plans to fit different needs and budgets. See our Pricing page for details.",
                "category": "Pricing",
                "display_order": 5,
                "is_active": True,
            },
            {
                "question": "Will my website be mobile-friendly?",
                "answer": "Yes, all our websites are fully responsive and optimized for mobile devices.",
                "category": "Technical",
                "display_order": 6,
                "is_active": True,
            },
            {
                "question": "How do I get started?",
                "answer": "Contact us through our website or call us to discuss your project and get a free quote.",
                "category": "Process",
                "display_order": 7,
                "is_active": True,
            },
        ]
        for faq in faqs:
            FAQ.objects.create(**faq)
        self.stdout.write(self.style.SUCCESS('FAQs populated!'))
