from tkinter import image_names
from django.shortcuts import render
from matplotlib.style import context
from .models import *
from django.http import HttpResponse
from .aiModel import *
import re
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import Image
from .serializers import ImageSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from rest_framework.response import Response
from requests_toolbelt.multipart import MultipartDecoder
from .forms import *
import PIL.Image


# Create your views here.
def index(request):
    #read image from computer
    path=plt.imread("C:\\Users\\Hussa\\Desktop\\TF2\\Experiment\\Raw Data\\Test\\IMG_5456.jpg")
    faculty_name=return_faculty_name(path)

    updated_faculty_name=re.sub('[123]',"",faculty_name)

    updated_faculty_name=updated_faculty_name.lower()

    faculties_ids={
        "kasit":1,
        "medicine":2,
        "engineering":3,
        "shareeah":4,
        "business":5,
        "law":7,
        "kitchen":8,
        'none':10,
    }

    #get faculty id
    faculty_id = faculties_ids[faculty_name]

    if faculty_id == 10:
        return render(request,'TEMP.html')
    
    facility = Faculty.objects.get(id=faculty_id)
    employees=Employee.objects.filter(department_employees__faculty_id=facility.id)[:5]
    
    return render(request,'index.html',{'emps':employees,'data':facility})

#returns the right data referring to the right faculty

#EmployeeAndDepartmentList
#Model.objects.model._meta.db_table
class EmployeeAndDepartmentList(APIView):
    # def get(self, request):
    #     #all employees
    #     # multipart_file = request.POST.get('image')
    #     #parsed = MultiPartParser.parse(multiPartFile)
    #     img = PIL.Image.open(request.data.get('image'))
    #     fac_id = return_faculty_id(img)

    #     if fac_id == 0:
    #         table = DepartmentEmployeeTable()
    #         table.name = 'None'
    #         tableList = [table, DepartmentEmployeeTable()]
    #         serializer = DepartmentEmployeeSerializer(tableList, many=True, context={'request' : request})

    #         content = {
    #             'employee' : serializer.data
    #         }
    #         return Response(content)
            

    #     facultyData = Faculty.objects.get(id=2)
    #     emp_db_name = Employee.objects.model._meta.db_table
    #     dep_db_name = Department.objects.model._meta.db_table

    #     #join tables department and employee according to faculty id and put them in a temporary model DepartmentEmployeeTable
    #     querySet = DepartmentEmployeeTable.objects.raw(f'SELECT {emp_db_name}.id, {emp_db_name}.first_name, {emp_db_name}.last_name, {emp_db_name}.office_place1, {dep_db_name}.office_place, {dep_db_name}.name FROM {dep_db_name}\
    #     INNER JOIN {emp_db_name} ON {dep_db_name}.faculty_id = {2} AND {emp_db_name}.department_employees_id = {dep_db_name}.id')        
    #     #employeeData = Employee.objects.filter(department_employees__faculty_id=facultyData.id) 
        
    #     #converts to JSON
    #     serializer_context = {
    #         'request': request,
    #     }
        
    #     #employeeSerializer = EmployeeSerializer(employeeData, many=True,context=serializer_context)
    #     departmentEmployeeSerializer = DepartmentEmployeeSerializer(querySet, many=True, context=serializer_context)
    #     facultySerializer = FacultySerializer(facultyData, many=False, context=serializer_context)
        
    #     content = {
    #         'faculty': facultySerializer.data,
    #         #'employee': employeeSerializer.data,
    #         'employee' : departmentEmployeeSerializer.data
    #     }

    #     #send temporary model back to client
    #     return Response(content)


    def post(self, request):
        #all employees
        # multipart_file = request.POST.get('image')
        #parsed = MultiPartParser.parse(multiPartFile)
        img = PIL.Image.open(request.data.get('image'))
        fac_id = return_faculty_id(img)

        # if fac_id == 0:
        #     table = DepartmentEmployeeTable()
        #     table.name = 'None'
        #     tableList = [table, DepartmentEmployeeTable()]
        #     serializer = DepartmentEmployeeSerializer(tableList, many=True, context={'request' : request})

        #     content = {
        #         'employee' : serializer.data
        #     }
        #     return Response(content)
            

        facultyData = Faculty.objects.get(id=8)
        emp_db_name = Employee.objects.model._meta.db_table
        dep_db_name = Department.objects.model._meta.db_table
        for field in Faculty.objects.values('id', 'name'):
            print(field)

        #join tables department and employee according to faculty id and put them in a temporary model DepartmentEmployeeTable
        querySet = DepartmentEmployeeTable.objects.raw(f'SELECT {emp_db_name}.id, {emp_db_name}.first_name, {emp_db_name}.last_name, {emp_db_name}.office_place1, {dep_db_name}.office_place, {dep_db_name}.name FROM {dep_db_name}\
        INNER JOIN {emp_db_name} ON {dep_db_name}.faculty_id = {8} AND {emp_db_name}.department_employees_id = {dep_db_name}.id')        
        #employeeData = Employee.objects.filter(department_employees__faculty_id=facultyData.id) 
        
        #converts to JSON
        serializer_context = {
            'request': request,
        }
        
        #employeeSerializer = EmployeeSerializer(employeeData, many=True,context=serializer_context)
        departmentEmployeeSerializer = DepartmentEmployeeSerializer(querySet, many=True, context=serializer_context)
        facultySerializer = FacultySerializer(facultyData, many=False, context=serializer_context)
        
        content = {
            'faculty': facultySerializer.data,
            #'employee': employeeSerializer.data,
            'employee' : departmentEmployeeSerializer.data
        }

        #send temporary model back to client
        return Response(content)


# def faculty_image_view(request):
  
#     if request.method == 'POST':
#         form = Faculty_Image(request.POST, request.FILES)  
#         if form.is_valid():
#             form.save()
#             return redirect('success')
#     else:
#         form = Faculty_Image()
#     return render(request, 'index.html', {'form' : form})
  
  
# def success(request):
#     return HttpResponse('successfully uploaded')
class FacultyViewSet(viewsets.ModelViewSet):

    # API endpoint that allows users to be viewed or edited.
        queryset = Faculty.objects.all()
        serializer_class = FacultySerializer
        permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):

    # API endpoint that allows users to be viewed or edited.
        queryset = Department.objects.all()
        serializer_class = DepartmentSerializer
        permission_classes = [permissions.IsAuthenticated]

class employeeViewSet(viewsets.ModelViewSet):

    # API endpoint that allows users to be viewed or edited.
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer
        permission_classes = [permissions.IsAuthenticated]

class DepartmentEmployeeViewSet(viewsets.ModelViewSet):
    # API endpoint that allows users to be viewed or edited.
    queryset = DepartmentEmployeeTable.objects.all()
    serializer_class = DepartmentEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
        
class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()