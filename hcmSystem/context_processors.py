from prodHCM.models import Profile


def global_variables(request):
    logo_url = ""
    profile = ""
    logo_color = ""
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        logo_url = profile.logo.url if profile.logo else None
        logo_color = profile.preferred_color if profile.preferred_color else None


    return {
        'insuranceCompany': getattr(request.user, 'insuranceCompany', None),
        'user_logo': logo_url,
        'profile': profile,
        'logo_color': logo_color,
    }