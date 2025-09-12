from django.core.management.base import BaseCommand
from core.models import PricingPlan

class Command(BaseCommand):
    help = 'Populate the PricingPlan table with demo data.'

    def handle(self, *args, **options):
        PricingPlan.objects.all().delete()
        plans = [
            {
                "name": "Starter",
                "price": 49.00,
                "billing_type": "monthly",
                "features": "Up to 5 pages\nBasic SEO\nResponsive Design\nEmail Support",
                "is_featured": False,
                "display_order": 1,
            },
            {
                "name": "Professional",
                "price": 99.00,
                "billing_type": "monthly",
                "features": "Up to 15 pages\nAdvanced SEO\nBlog Integration\nPriority Email Support\nCustom Forms",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "name": "Business",
                "price": 199.00,
                "billing_type": "monthly",
                "features": "Unlimited Pages\nE-Commerce\nPremium SEO\nAnalytics Dashboard\nPhone & Email Support\nCustom Integrations",
                "is_featured": False,
                "display_order": 3,
            },
            {
                "name": "One-Time Website",
                "price": 1200.00,
                "billing_type": "one_time",
                "features": "Up to 10 pages\nSEO Setup\n1 Year Hosting\nContact Form\nBasic Analytics",
                "is_featured": False,
                "display_order": 4,
            },
            {
                "name": "Annual Pro",
                "price": 999.00,
                "billing_type": "yearly",
                "features": "Unlimited Pages\nE-Commerce\nFull SEO Suite\nBlog & Newsletter\nDedicated Support\nFree Updates",
                "is_featured": True,
                "display_order": 5,
            },
            {
                "name": "Custom",
                "price": 344.44,
                "billing_type": "monthly",
                "features": "Unlimited Pages\nE-Commerce\nFull SEO Suite\nBlog & Newsletter\nDedicated Support\nFree Updates",
                "is_featured": True,
                "display_order": 6,
            }
        ]
        for plan in plans:
            PricingPlan.objects.create(**plan)
        self.stdout.write(self.style.SUCCESS('Pricing plans populated!'))
