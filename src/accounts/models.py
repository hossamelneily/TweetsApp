from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse_lazy,reverse
from django.db.models.signals import post_save,pre_save
from django.core.validators import RegexValidator
from django.utils.text import slugify
from autoslug import AutoSlugField
import os,random,sys,json
from django.utils import timezone
from location_field.models.plain import PlainLocationField

def content_file_name(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,'{0}{1}'.format(random.randint(0,sys.maxsize),os.path.splitext(filename)[1]) )

class MyUserManager(BaseUserManager):
    def create_user(self, email, username,password,first_name = None,last_name=None):
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
            first_name=first_name,
            last_name=last_name,

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


    # def following   user.profile.following.all
    # def all(self):
    #     print(self)
    #     print((self.get_queryset()))
    #     return self.get_queryset().exclude(username=self.username)

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

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=120,
        null=True,blank=True
    )
    last_name = models.CharField(
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

    def get_absolute_url(self):
        return reverse('accounts:profile',kwargs={'slug':self.slug})
        # return '{}/'.format(self.slug)

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

# class ProfileQs(models.query.QuerySet):
#     def all(self):
#         return self.user.following.exclude(username=self.user.username)  #self.user --> user (reverse relationship for the onetoone user <--> profile )

class ProfileManager(models.Manager):
    # def get_queryset(self):
    #     return ProfileQs(self.model,using=self._db)


    # use_for_related_fields = True


    def all(self):   #user.followed_by.all
        print(self)  # --> profile
        return self.get_queryset().exclude(user=self.instance) # user = reverse profile = self.instance



class Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to=content_file_name,verbose_name="Profile Picture")
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    following = models.ManyToManyField(MyUser,blank=True,related_name='followed_by')
    # city = models.CharField(max_length=255,default='kuwait')
    # location = PlainLocationField(based_fields=['city'], zoom=7,null=True)

    #N.B --> 1) user.profile.following.all() = i follow who
    #        2) user.followed_by.all()  = who follow me
    # def followed_by(self):
    #     return json.dumps(self.user.followed_by.all())
    objects = ProfileManager()
    def __str__(self):
        return self.user.username



    def get_following(self):
        return self.following.all().exclude(username=self.user.username)

def Create_Profile_receiver(sender,instance,created,*args,**kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(Create_Profile_receiver,MyUser)


# def Slugify_User(sender,instance,*args,**kwargs):
#     instance.slug=slugify(instance.username)
#
# pre_save.connect(Slugify_User,MyUser)

