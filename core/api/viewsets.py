import time

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import TotalOccurrencesSerializer, DataReceivedSerializer
from core.crawler import execute


class TotalOccurrencesAPIView(APIView):

    def get(self, request, format=None):
        start_time = time.time()
        data = self._parse_query_params(request.query_params)
        data_received = DataReceivedSerializer(data=data)

        if data_received.is_valid():
            urls = data_received.data.get('urls')
            word = data_received.data.get('word')
            response = execute(urls, word)
            print("Entire request took", time.time() - start_time, "seconds")
            return Response(TotalOccurrencesSerializer(response, many=True).data, status=status.HTTP_200_OK)
        return Response(data_received.errors, status=status.HTTP_400_BAD_REQUEST)

    def _parse_query_params(self, query_params):
        data = query_params.dict()
        urls = data.get('urls', [])
        if urls:
            data['urls'] = urls.split(',')
        else:
            data.pop('urls')
        print(data)
        return data
