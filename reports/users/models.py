import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True,)
    firstname = models.CharField('Имя', max_length=20)
    lastname = models.CharField('Фамилия', max_length=30, null=True)
    email = models.EmailField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, editable=False)

    objects = UserManager()
    # children = ChildrenManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their full name
        return str(self.firstname) + ' ' + str(self.lastname)

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.username

    def create_hash(self):
        now = datetime.now()
        s = str(now) + str(self.username) + str(self.email)
        h = hashlib.sha1(s.encode())
        return h.hexdigest()


# class RegistrationHash(models.Model):
#     user_id = ''
#     hash_link = ''
