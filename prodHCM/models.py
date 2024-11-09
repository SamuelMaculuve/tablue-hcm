from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=100)
    nuitNumber = models.CharField(max_length=15)
    phoneNumber = models.CharField(max_length=15)
    date_of_activity_start = models.DateField()
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    contractFile = models.FileField(upload_to='clients/')
    nuitFile = models.FileField(upload_to='clients/')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="subCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Procedure(models.Model):
    name = models.CharField(max_length=255)
    # supplier = models.ManyToManyField(Supplier, related_name="procedimentos")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name