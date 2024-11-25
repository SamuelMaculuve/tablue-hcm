def global_variables(request):
    return {
        'insuranceCompany': getattr(request.user, 'insuranceCompany', None)
    }