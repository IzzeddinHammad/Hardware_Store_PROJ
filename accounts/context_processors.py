def user_groups(request):
    if request.user.is_authenticated:
        return {'is_vendor': request.user.groups.filter(name='Vendor').exists()}
    return {'is_vendor': False}