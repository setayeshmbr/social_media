from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager) :
    use_in_migrations = True

    def _create_user(self, email, user_name, password=None, **extra_fields) :
        """
        Creates and saves a User with the given email and password.
        """
        if not email :
            raise ValueError('Users must have an email address')

        if not user_name :
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user_name = self.model.normalize_username(user_name)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, user_name, password=None, **extra_fields) :
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        user = self._create_user(
            email,
            user_name,
            password=password,
            **extra_fields
        )
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields) :
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self._create_user(
            email,
            user_name,
            password=password,
            **extra_fields
        )
        user.save(using=self._db)
        return user
