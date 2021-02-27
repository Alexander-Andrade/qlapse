from django.conf import settings


def site_url(path):
    return f"{settings.BASE_URL}/{path.lstrip('/')}"
