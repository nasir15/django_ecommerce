from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from .models import Product
import logging


class ProductAPI(APIView):
    # permission_classes = (IsAuthenticated, )
    logger = logging.getLogger('django')

    def get(self, request):
        try:
            products = Product.objects.all()
            print("products ",products)
            serializer = ProductSerializer(products, many=True)
            print("Serializer data",serializer.data)
            base_url="http://192.168.53.105:8080"
            for i in serializer.data:
                if i.get('image') is not None:
                    i['image']=base_url+i.get('image')
                       
            return Response(serializer.data, status=200)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)

