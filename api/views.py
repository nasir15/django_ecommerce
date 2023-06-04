from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from .models import Product


class ProductAPI(APIView):
    # permission_classes = (IsAuthenticated, )
    # logger = logging.getLogger('django')

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            base_url="http://192.168.53.105:8080"
            print(serializer.data)
            for i in serializer.data:
                i['image']=base_url+i.get('image')
            
            return Response(serializer.data, status=200)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)

