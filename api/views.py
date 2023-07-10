from django.shortcuts import render

# Create your views here.
from pymongo import MongoClient
from .models import IData
from django.http import HttpResponse

from rest_framework import viewsets
from api.models import IData
from api.serializers import IDataSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

def insert_data(request):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    db = client['phonedata']
    collection = db['records']

    # Read data from MongoDB
    data = collection.find()
    # print("this is my data",data[1])
    # print("type",type(data[1]))
    # print(type(data[1]["dd"]))
    # Insert data into the IData model
    # for item in data:
    #     i_data = IData(
    #         field1=item['field1'],
    #         field2=item['field2'],
    #         field3=item['field3']
    #     )
    #     i_data.save()

    return HttpResponse('Data inserted successfully!')
    # return HttpResponse(data[1]["dd"])
 

class IDataViewSet(viewsets.ModelViewSet):
    queryset= IData.objects.all()
    serializer_class=IDataSerializer

    @action(detail=False, methods=['GET'], url_path='get-version')
    def get_version(self, request): 
        companies = self.queryset
        versions = [company.vn for company in companies]  # Extract 'dd' field values

        response_data = {
            "status": "versions extracted successfully",
            "payload": versions
        }
        #return Response(serializer.data)
        return Response(response_data)
