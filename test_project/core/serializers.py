from rest_framework import serializers 
from .models import *
from rest_flex_fields import FlexFieldsModelSerializer


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields ='__all__'


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'


class DepartmentEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DepartmentEmployeeTable
        fields = '__all__'

from .models import Image
from versatileimagefield.serializers import VersatileImageFieldSerializer


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Image
        fields = ['pk','image']




