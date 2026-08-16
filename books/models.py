from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField()
    
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author,on_delete=models.RESTRICT,related_name='books')
    category =  models.ForeignKey(Category,on_delete=models.RESTRICT)
    isbn = models.CharField(max_length=100,unique=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title
    