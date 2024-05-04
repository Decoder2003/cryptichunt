from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from home.models import cryptUser, CryptManager

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password = None, **kwargs):
        UserModel = cryptUser
        print(username, password)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            print(case_insensitive_username_field)
            user = UserModel.objects.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            print('going here')
            print(user, password)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user