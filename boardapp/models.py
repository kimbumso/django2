from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class UserManager(BaseUserManager):
    def create_user(self, username, password, last_name, email, phone, date_of_birth):
        user = self.model(
            username=username,
            last_name=last_name,
            email=self.normalize_email(email),
            phone=phone,
            date_of_birth=date_of_birth,
            date_joined=timezone.now(),
            is_superuser=0,
            is_staff=0,
            is_active=1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, last_name, email, phone, date_of_birth, password):
        user = self.create_user(
            username=username,
            password=password,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth
        )
        user.is_superuser=1
        user.is_staff=1
        user.save(using=self._db)
        return user
        
class User(AbstractBaseUser):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    is_superuser = models.IntegerField()
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=254)
    date_of_birth = models.DateTimeField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name', 'phone', 'email', 'date_of_birth']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'auth_user'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class BoardCategories(models.Model):
    category_type = models.CharField(max_length=45)
    category_code = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    category_desc = models.CharField(max_length=200)
    list_count = models.IntegerField(blank=True, null=True)
    authority = models.IntegerField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.category_name, self.category_code)

    class Meta:
        managed = False
        db_table = 'board_categories'


class Boards(models.Model):
    category = models.ForeignKey(BoardCategories, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=300)
    #content = RichTextField(blank=True, null=True)
    content= RichTextUploadingField(blank=True, null=True)
    #content = RichTextUploadingField(blank=True, null=True, config_name='awesome_ckeditor')
    registered_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    last_update_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True, default=0)
    image = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '[%d] %.40s' % (self.id, self.title)
    
    class Meta:
        managed = False
        db_table = 'boards'


class BoardReplies(models.Model):
    article = models.ForeignKey(Boards, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    level = models.IntegerField(blank=True, null=True)
    #content = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    #content = RichTextUploadingField(blank=True, null=True, config_name='awesome_ckeditor')
    reference_reply_id = models.IntegerField(blank=True, null=True)
    registered_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '[%d] %.40s - [%d] %.40s' % (self.article.id, self.article.title, self.id, self.content)
    
    class Meta:
        managed = False
        db_table = 'board_replies'


class BoardLikes(models.Model):
    article = models.ForeignKey(Boards, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    registered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '[%d] %.40s - %s' % (self.article.id, self.article.title, self.user.last_name)
    
    class Meta:
        managed = False
        db_table = 'board_likes'
# Unable to inspect table 'board_images'
# The error was: (1146, "Table 'awsdjangodb.board_images' doesn't exist")
