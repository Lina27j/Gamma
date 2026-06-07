from .models import CompanyProfile


def company_profile(request):
    return {'company': CompanyProfile.objects.first()}
