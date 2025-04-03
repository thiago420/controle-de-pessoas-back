from django.db import models

class User():
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
