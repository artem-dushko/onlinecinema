from django.db import models

class Video(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('Sci-Fi', 'Science Fiction (Sci-Fi)'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Crime', 'Crime'),
        ('Historical', 'Historical'),
        ('Musical', 'Musical'),
        ('Documentary', 'Documentary'),
        ('Animated', 'Animated'),
        ('Western', 'Western'),
        ('War', 'War'),
    ]

    video_file = models.FileField(upload_to='videos/')
    placeholder_image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=30)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    description = models.CharField(max_length=250)
    duration = models.CharField(max_length=5)
    cast = models.CharField(max_length=250)
    year = models.IntegerField(default=2024)
    date_added = models.DateField(auto_now_add=True)