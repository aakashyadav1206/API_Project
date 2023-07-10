from rest_framework import serializers
from api.models import IData


#create serializers here
class IDataSerializer(serializers.HyperlinkedModelSerializer):
    company_id=serializers.ReadOnlyField()
    class Meta:
        model=IData
        fields="__all__"
