from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%y/%m/%d')
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    date = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)

    def __str__(self):
        return f"{self.title}  ->  {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    posted_by = models.CharField(max_length=100, default='admin')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body