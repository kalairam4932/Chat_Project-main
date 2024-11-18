from django.db import models
from PIL import Image

# Create your models here.

# UserAccounts
class UserAccount(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length = 100)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    is_active = models.BooleanField(default = True)
    profile_pic = models.ImageField(default = 'default_profile.jpg', upload_to = 'profile_pics')

    def __str__(self) -> str:
        return self.firstname
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.profile_pic.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)

    @property
    def is_authenticated(self) -> bool:
        return True

# Private Conversations
class Conversations(models.Model):
    mainuser = models.ForeignKey(UserAccount, on_delete = models.DO_NOTHING, related_name = 'main')
    seconduser = models.ForeignKey(UserAccount, on_delete = models.DO_NOTHING, related_name = 'secondary')
    is_blocked = models.BooleanField(default = False)
    conv_id = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return self.conv_id
    
# Messages
class Message(models.Model):
    user = models.CharField(max_length = 100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    is_deleted = models.BooleanField(default = False)
    conv_id = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.conv_id



