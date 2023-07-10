import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from api.models import IData
IData.objects.all().delete()
file_path = 'raw.txt'
with open(file_path, 'r') as file:
    raw_data = file.readlines()

try:
    for line in raw_data:
        data = eval(line.strip()) 
        #print(data)  
        instance = IData(**data)
        instance.save()
except Exception as e:
    print(f"An error occurred during data insertion: {str(e)}")
