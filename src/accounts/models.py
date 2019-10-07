from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save,pre_save
from django.core.validators import RegexValidator
from django.utils.text import slugify
from autoslug import AutoSlugField


def content_file_name(instance,filename):
    return 'user_{0}/{1}'.format(instance.id, filename)

class MyUserManager(BaseUserManager):
    def create_user(self, email, username,password,firstname = None,lastname=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have unique Username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

UsernameRegex = '^[a-zA-Z0-9.@+-]*$'

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,error_messages={'unique':'This Email Address is already registered '}
    )
    username = models.CharField(unique=True,
        verbose_name='UserName', max_length=120,validators=
        [
            RegexValidator(regex=UsernameRegex,
            message="The username must be Aplanumeric or contain any of the following @ . - +",code='Invalid UserName')]
    ,error_messages={'unique':'This Username is already registered '})

    slug = AutoSlugField(null=True,populate_from='username',max_length=120,unique=True)

    firstname = models.CharField(
        verbose_name='First Name',
        max_length=120,
        null=True,blank=True
    )
    lastname = models.CharField(
        verbose_name='Last Name',
        max_length=120,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)




    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin




class Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to=content_file_name,verbose_name="Profile Picture")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username





def Create_Profile_receiver(sender,instance,created,*args,**kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(Create_Profile_receiver,MyUser)


# def Slugify_User(sender,instance,*args,**kwargs):
#     instance.slug=slugify(instance.username)
#
# pre_save.connect(Slugify_User,MyUser)

