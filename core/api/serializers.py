from rest_framework import serializers
from collections import namedtuple


class TotalOccurrencesSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)
    word = serializers.CharField(max_length=50)
    total_occurrences = serializers.IntegerField()

class DataReceivedSerializer(serializers.Serializer):
    urls = serializers.ListField()
    word = serializers.CharField()

