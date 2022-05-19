from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


# Create your models here.

class Faculty(models.Model):
    name=models.CharField(max_length=20)
    faculty_dean=models.CharField(max_length=40,default='none')
    faculty_info=models.TextField(default="unknown")
    established_date=models.IntegerField(default=2000)
    def __str__(self):
        return self.name

class Department(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    office_place=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    department_employees=models.ForeignKey(Department,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    office_place1=models.CharField(max_length=50,default='None')
    

    def __str__(self):
        return self.first_name
# class Faculty_Image(models.Model):
#     faculty_imge=models.ImageField(upload_to='images/')

class DepartmentEmployeeTable(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    office_place=models.CharField(max_length=50)
    office_place1=models.CharField(max_length=50)
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.department_name


class Image(models.Model):
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

