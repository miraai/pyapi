from django.db import models

class User(models.Model):
  email = models.CharField(max_length=100, blank=False, unique=True, required=True)
  password = models.CharField(max_length=100, blank=False, required=True)
  created_at = models.DateTimeField(auto_now_add=True)
 
  class Meta:
        db_table = 'user'

class Posts(models.Model):
  subject = models.CharField(max_length=20, blank=False)
  content = models.CharField(max_length=245, blank=False)
  deleted = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
        db_table = 'posts'

class PostsLike(models.Model):
  liked = models.BooleanField(default=True)
  post = models.ForeignKey(Posts, on_delete=models.CASCADE, db_column='post_id')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
        db_table = 'posts_like'