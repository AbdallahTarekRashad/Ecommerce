import requests
from .models import User
from django.core import files
from io import BytesIO


def save(backend, user, response, *args, **kwargs):
    flag = False
    if backend.name == "facebook":
        flag = True
        pic_url = response['picture']['data']['url']
        first_name = response['first_name']
        last_name = response['last_name']
    elif backend.name == 'google-oauth2':
        flag = True
        pic_url = response['picture']
        pic_url = pic_url.split('=')[0] + '=s500'
        first_name = response['given_name']
        last_name = response['family_name']

    if flag:
        u = User.objects.filter(pk=user.pk)
        if u is not None:
            u = u.first()
            if backend.name == "facebook":
                u.username = response['email'].split('@')[0]
            u.first_name = first_name
            u.last_name = last_name
            resp = requests.get(pic_url)
            # stream image and save in media dir and add to user
            if resp.status_code == 200:
                fp = BytesIO()
                fp.write(resp.content)
                file_name = 'image.jpeg'
                u.image.save(file_name, files.File(fp), save=True)
            if response.get('gender', None):
                if response['gender'] == 'male':
                    u.gender = 0
                else:
                    u.gender = 1
            u.save()

