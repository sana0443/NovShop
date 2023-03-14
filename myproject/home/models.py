from django.db import models
from django.utils.safestring import mark_safe 
from django.contrib.auth.models import User


class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()

# class UserDetail(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     mobile=models.CharField(max_length=10,null=True) 


class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(blank=True,max_length=50)
    phone = models.CharField(blank=True,max_length=50)
    address = models.CharField(blank=True,max_length=50)
    postcode = models.CharField(blank=True,max_length=15)
    state = models.CharField(blank=True,max_length=50)
    city = models.CharField(blank=True,max_length=50)
    email = models.EmailField(blank=True,max_length=250)
    country = models.CharField(blank=True,max_length=50)
    phone2 = models.CharField(blank=True,max_length=50)
    image = models.ImageField(upload_to='images/users/')
    primary_address=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)


    def _str_(self):
        return self.user.username
    def user_name(self):
        return self.user.first_name+ '' + self.user.last_name + '['+self.user.username+']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'image'      

    # def __str__(self)
        # return self.username.username
       

# class User(AbstractUser):
#     # other fields and methods if any
#     def create_user(self, username, email, password):
#         user = self.model(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
#         return user
#         groups = models.ManyToManyField(Group, related_name='home_user_groups')


