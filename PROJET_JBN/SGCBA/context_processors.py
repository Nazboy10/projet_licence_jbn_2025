from SGCBA.models import Utilisateur

def user_photo(request):
    if 'id' in request.session:
        try:
            user = Utilisateur.objects.get(id=request.session['id'])
            return {'user_photo': user.photo.url, 'username': user.username, 'role': user.role}
        except Utilisateur.DoesNotExist:
            return {'user_photo': '/static/image/pro.png', 'username': '', 'role': ''}
    return {'user_photo': '/static/image/pro.png', 'username': '', 'role': ''}
