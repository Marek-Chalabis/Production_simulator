from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50, default='Warszawa', choices=(
        ('Warszawa', 'Warszawa'), ('Lublin', 'Lublin'), ('Radom', 'Radom'), ('Gdynia', 'Gdynia'), ('Kraków', 'Kraków')))
    image = models.ImageField(default='profile_image/default_profile.jpg', upload_to='profile_image')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # overwrite save to change uploaded image
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            compresed_size = (250, 250)
            img.thumbnail(compresed_size)
            img.save(self.image.path)
