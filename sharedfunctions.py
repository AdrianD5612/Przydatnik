from wydatki.models import Theme

def theme(request): #wybranie motywu
    mode=request.GET.get('mode')

    if mode=='dark':
        if Theme.objects.filter(user_theme=request.user).exists():
            user_saving= Theme.objects.get(user_theme=request.user)
            user_saving.user_theme=request.user
            user_saving.mode='dark'
            user_saving.save()
        else:
            user2=Theme(user_theme=request.user, mode='dark')
            user2.save()
    elif mode=='white':
        if Theme.objects.filter(user_theme=request.user).exists():
            user_saving= Theme.objects.get(user_theme=request.user)
            user_saving.user_theme=request.user
            user_saving.mode='white'
            user_saving.save()
        else:
            user2=Theme(user_theme=request.user, mode='white')
            user2.save()