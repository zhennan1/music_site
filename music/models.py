from django.db import models

class Singer(models.Model):
    singer_id = models.CharField(max_length=50, unique=True)
    singer_name = models.CharField(max_length=100)
    image_url = models.URLField()
    bio = models.TextField()
    original_url = models.URLField()

    def __str__(self):
        return self.singer_name

class Song(models.Model):
    song_id = models.CharField(max_length=50, unique=True)
    song_name = models.CharField(max_length=100)
    singer = models.ForeignKey(Singer, related_name='songs', on_delete=models.CASCADE)
    image_url = models.URLField()
    lyrics = models.TextField(blank=True, null=True)
    original_url = models.URLField()

    def __str__(self):
        return self.song_name

class Comment(models.Model):
    song = models.ForeignKey(Song, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.song.song_name} by {self.created_at}'
