from django.db import models

class User(models.Model):
    id       = models.CharField(max_length = 50, unique = True, primary_key = True)
    password = models.CharField(max_length = 200)
    trims    = models.ManyToManyField('trims.Trim', through = 'UserTrim')

    class Meta:
        db_table = 'users'

class UserTrim(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    trim = models.ForeignKey('trims.Trim', on_delete = models.CASCADE)

    class Meta:
        db_table = 'users_trims'