from django.shortcuts import render
import datetime
from datetime import datetime as dt
# Create your views here.
from pymongo import MongoClient
from .models import IData
from django.http import HttpResponse
#from datetime import datetime
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
        companies = self.queryset.values('vn').distinct()
        companies2 = self.queryset.values()
        print(companies2[0])
        #versions = [company for company in companies]  # Extract 'dd' field values

        response_data = {
            "status": "versions extracted successfully",
            "payload": companies
        }
        #return Response(serializer.data)
        return Response(response_data)

    @action(detail=False, methods=['GET'], url_path='get-dd')
    def get_dd(self, request): 
        companies = self.queryset.values('dd').distinct()

        #versions = [company for company in companies]  # Extract 'dd' field values

        response_data = {
            "status": "Device ids extracted successfully",
            "payload": companies
        }
        #return Response(serializer.data)
        return Response(response_data)
     
    @action(detail=False, methods=['GET'], url_path='get-version-on-date')
    def get_version_on_date(self, request): 
        date_string = request.GET.get('date')
        companies = self.queryset.values()

        #versions = [company for company in companies]  # Extract 'dd' field values
        #companies=datetime.datetime.fromtimestamp(companies)
        version=set()
        my_dict = {}
        for i in companies:
            #i=datetime.datetime.fromtimestamp(i["ep"])
            #print(i)
            #if i.date()==datetime.strptime(date_string, "%d-%m-%Y").date():
                #version.append(i['vn'])
            dd = dt.fromtimestamp(i["ep"])
            
            if dd.date() in my_dict:
                my_dict[dd.date()].add(i['vn'])
            else:
                my_dict[dd.date()] = {i['vn']}
            if dd.date() == dt.strptime(date_string, "%d-%m-%Y").date():
                #print(i)
                #print(type(i))
                version.add(i['vn'])
        #print(my_dict)
        response_data = {
            "status": "Device ids extracted successfully",
            "payload": version
        }
        #return Response(serializer.data)
        return Response(response_data)



    @action(detail=False, methods=['GET'], url_path='get-days-1-less-(?P<n>\d+)-data')
    def get_days(self, request, n): 
        #n = int(request.GET.get('n'))
        #date_string = request.GET.get('date')
        #n=2
        n=int(n)
        companies = self.queryset.values()

        #versions = [company for company in companies]  # Extract 'dd' field values
        #companies=datetime.datetime.fromtimestamp(companies)
        version=0
        my_dict = {}
        for i in companies:
            dd = dt.fromtimestamp(i["ep"])
            
            if dd.date() in my_dict:
                my_dict[dd.date()].add(i['vn'])
            else:
                my_dict[dd.date()] = {i['vn']}
        #print(my_dict)
        for date, cnt in my_dict.items():
            print(date, ":", len(cnt),'\n')
            if len(cnt)==n-1:
                version=version+1

        response_data = {
            "status": "Device ids extracted successfully",
            "payload": version
        }
        #return Response(serializer.data)
        return Response(response_data)
       

    @action(detail=False, methods=['GET'], url_path='get-highest-values')
    def get_highest_values(self, request): 
        date_string = request.GET.get('date')
        companies = self.queryset.values()

        #versions = [company for company in companies]  # Extract 'dd' field values
        #companies=datetime.datetime.fromtimestamp(companies)
        version=[]
        tm=0
        hm=0
        my_dict = {}
        for i in companies:
            #i=datetime.datetime.fromtimestamp(i["ep"])
            #print(i)
            #if i.date()==datetime.strptime(date_string, "%d-%m-%Y").date():
                #version.append(i['vn'])
            dd = dt.fromtimestamp(i["ep"])
            
            if dd.date() in my_dict:
                my_dict[dd.date()].add(i['vn'])
            else:
                my_dict[dd.date()] = {i['vn']}
            if dd.date() == dt.strptime(date_string, "%d-%m-%Y").date():
                #print(i)
                #print(type(i))
                print(i['dt']['tm'],i['dt']['tm'])
                tm=max(tm,i['dt']['tm'])
                hm=max(hm,i['dt']['hm'])
        #print(my_dict)
        print(tm,hm)
        version={}
        version['tm']=tm
        version['hm']=hm
        response_data = {
            "status": "Device ids extracted successfully",
            "payload": version
        }
        #return Response(serializer.data)
        return Response(response_data)

    @action(detail=False, methods=['GET'], url_path='get-data-points')
    def get_data_points(self, request): 
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        vn = request.GET.get('vn')
        companies = self.queryset.values()
        #did not include start and end date

        #versions = [company for company in companies]  # Extract 'dd' field values
        #companies=datetime.datetime.fromtimestamp(companies)
        version=[]
        tm=0
        hm=0
        cnt=0
        my_dict = {}
        sdate=dt.strptime(start_date, "%d-%m-%Y")
        edate=dt.strptime(end_date, "%d-%m-%Y")
        print(sdate,edate)
        print(vn)
        vvn=set()
        ccn=0
        for i in companies:
            #i=datetime.datetime.fromtimestamp(i["ep"])
            #print(i)
            #if i.date()==datetime.strptime(date_string, "%d-%m-%Y").date():
                #version.append(i['vn'])
            dd = dt.fromtimestamp(i["ep"])
            
            if dd.date() in my_dict:
                my_dict[dd.date()]= my_dict[dd.date()]+1
            else:
                my_dict[dd.date()] = 1
            #if dd.date() == dt.strptime(date_string, "%d-%m-%Y").date():
                #print(i)
                #print(type(i))
                #print(i['dt']['tm'],i['dt']['tm'])
                #tm=max(tm,i['dt']['tm'])
                #hm=max(hm,i['dt']['hm'])
            
            if sdate <= dd <= edate:
                print("vn ==",i['vn'])
                ccn=ccn+1
            if (sdate <= dd <= edate) and vn[1:len(vn)-1]==i['vn']:
                cnt=cnt+1
        #print(vvn)
        #print(type(vn),vn)
        print(my_dict)
        print("ccn = ",ccn)
        version={}
        version['datapoints']=cnt
        response_data = {
            "status": "Device ids extracted successfully",
            "payload": version
        }
        #return Response(serializer.data)
        return Response(response_data)

    @action(detail=False, methods=['POST'], url_path='convert-version')
    def convert_version(self, request):
        dataepoch = request.data['dataepoch']
        dd = request.data['dd']
        new_vn = request.data['new_vn']
        
        data_point = self.queryset.filter(ep=dataepoch, dd=dd).first()
        if not data_point:
            return Response({'error': 'Data point not found'})

        data_point.vn = new_vn
        data_point.save()
        
        response_data = {
            "status": "Datapoint successfully updated with new version",
        }

        # Return a success response
        return Response(response_data)

    @action(detail=False, methods=['POST'], url_path='exchange-tm-hm')
    def exchange_tm_hm(self, request):
        dataepoch = request.data['dataepoch']
        dd = request.data['dd']

        data_point = self.queryset.filter(ep=dataepoch, dd=dd).first()
        if not data_point:
            return Response({'error': 'Data point not found'})
        
        tm=data_point.dt['tm']
        hm=data_point.dt['hm']
        print("tm =",tm)
        print("hm =",hm)
        #data_point.vn = new_vn
        #data_point.save()
        data_point.dt['tm']=hm
        data_point.dt['hm']=tm
        data_point.save()
        response_data = {
            "status": "tm and hm in data point are successfully exchanged",
        }

        # Return a success response
        return Response(response_data)

    @action(detail=False, methods=['DELETE'], url_path='delete-data-point')
    def delete_data_point(self, request):
        dataepoch = request.data['dataepoch']
        dd = request.data['dd']

        data_point = self.queryset.filter(ep=dataepoch, dd=dd).first()
        if not data_point:
            return Response({'error': 'Data point not found'})

        data_point.delete()
        response_data = {
            "status": "Datapoint deleted succesfully",
        }

        # Return a success response
        return Response(response_data)

