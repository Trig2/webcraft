from .models import SiteSetting


def site_settings(request):
    site_setting = SiteSetting.objects.first()
    if site_setting:
        return {
            "site_name": site_setting.site_name,
            "facebook": site_setting.facebook,
            "twitter": site_setting.twitter,
            "instagram": site_setting.instagram,
            "linkedin": site_setting.linkedin,
            "mail": site_setting.contact_email,
            "tel": site_setting.contact_phone,
            "address": site_setting.address,
            "logo": site_setting.logo,
            "about": site_setting.about,
        }
    return {}
