from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProductListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Требуется авторизация. Получите токен через /api/auth/login/'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        products = [
            {'id': 1, 'name': 'Ноутбук', 'price': 50000},
            {'id': 2, 'name': 'Смартфон', 'price': 30000},
            {'id': 3, 'name': 'Планшет', 'price': 20000},
        ]

        return Response({
            'products': products,
            'message': f'Добро пожаловать, {request.user.email}!'
        })


class OrderListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Требуется авторизация'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        orders = [
            {'id': 1, 'product': 'Ноутбук', 'status': 'доставлен'},
            {'id': 2, 'product': 'Смартфон', 'status': 'в обработке'},
            {'id': 3, 'product': 'Планшет', 'status': 'отменен'},
        ]

        return Response({
            'orders': orders,
            'message': f'Заказы пользователя {request.user.email}'
        })