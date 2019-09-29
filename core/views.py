from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token

import webscraper.scrapersSCR as scrapersSCR
import webscraper.timerSCR as timerSCR


# CHECK IF EMAIL EXIST IN DB (READY)
class CheckEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        response = {'message': 'free'}
        uEmail = request.data.get('email')

        username_list = User.objects.all()

        for existUser in username_list:
            print(existUser.email)
            if existUser.email == uEmail:
                response = {'message': 'exist'}

        return Response(response, status.HTTP_200_OK)


# CHECK IF USERNAME EXIST IN DB (READY)
class CheckUsername(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        response = {'message': 'free'}
        uName = request.data.get('username')

        username_list = User.objects.all()

        for existUser in username_list:
            print(existUser.username)
            if existUser.username == uName:
                response = {'message': 'exist'}

        return Response(response, status.HTTP_200_OK)


# LOGOUT USER FROM ALL DEVICES - DELETE TOKEN
class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()


#
#   ##        #   ###########   ###########   ###########
#   ##        #   ##            ##            ##        #
#   ##        #   ###########   ###########   ###########
#   ##        #             #   ##            ##    #
#   ##        #             #   ##            ##     #
#   ###########   ###########   ###########   ##      #
#


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Return data of signed in user
        :return:
        """
        user_id = self.request.user.id
        user = User.objects.filter(id=user_id)

        return user

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        email_req = request.query_params.get('email')
        username_req = request.query_params.get('username')
        password_req = request.query_params.get('password')

        user = User.objects.create_user(
            email=email_req,
            username=str(username_req),
            password=password_req,
        )
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # [task] set user inactive
        user = self.get_object()
        user.is_active = False
        user.save()

        # [var]products to set inactive
        inactive_prod = []

        # [task] set all connectors connected to user inactive
        user_id_str = str(user.id)
        user_id = int(user_id_str)

        connectors = Connector.objects.filter(user_id=user_id)
        connectors.update(is_active=False)
        for conn in connectors:
            inactive_prod.append(str(conn.productId))
            conn.save()

        # [task] set all product watched by user inactive
        for prod_id in inactive_prod:
            product = Product.objects.filter(id=int(prod_id))
            product.update(is_active=False)
            for item in product:
                item.save()

        return Response({"Message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)


#
#   ###########   ###########   ###########   ###########   ###########
#   ##                 ##       ##        #   ##        #   ##
#   ###########        ##       ##        #   ###########   ###########
#             #        ##       ##        #   ##   #        ##
#             #        ##       ##        #   ##    #       ##
#   ###########        ##       ###########   ##     #      ###########
#

class StoreViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = StoreSerializer

    def get_queryset(self):
        """
        Returns list of all stores or list of stores from particular country
        :return:
        """
        store_list = Store.objects.all()
        country_val = self.request.query_params.get('country', None)

        if country_val is not None:
            store_list = store_list.filter(country=country_val)

        return store_list


#
#   ###########   ###########   ###########   ########      ##        #   ###########   ###########
#   ##        #   ##        #   ##        #   ##       #    ##        #   ##                 ##
#   ###########   ###########   ##        #   ##        #   ##        #   ##                 ##
#   ##            ##    #       ##        #   ##        #   ##        #   ##                 ##
#   ##            ##     #      ##        #   ##       #    ##        #   ##                 ##
#   ##            ##      #     ###########   ########      ###########   ###########        ##
#


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Return list of all active products
        :return:
        """
        products_list = Product.objects.filter(is_active=True)
        return products_list

    def list(self, request, *args, **kwargs):
        """
        List only products users watching
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        user_id = self.request.user.id
        connector_data = Connector.objects.filter(user_id=user_id, is_active=True)
        product_list_to_display = []

        for connector in connector_data:
            product_list_to_display.append(connector.product)

        serializer = ProductSerializer(product_list_to_display, many=True)

        return Response(serializer.data)

    # POST
    def create(self, request, *args, **kwargs):
        user_id = request.user.id

        product_url = request.data.get('url')
        storeID = request.data.get('store_id')

        # Scrap data
        scraper = scrapersSCR.XkomScraper()
        scraper.set_product_url(product_url)

        name = scraper.get_product_name()
        price = scraper.get_product_price()
        date = timerSCR.get_current_datetime()

        print('------------- NEW PRODUCT -----------------')
        print(name)
        print(price)
        print(date)

        # Create New Product
        product_new = Product.objects.create(
            name=name,
            url=product_url,
            urlToBuy=product_url,
            priceStart=price,
            priceCurrent=price,
            priceHighest=price,
            priceLowest=price,
            dateAdded=date,
            dateLastChecked=date,
            dateHighest=date,
            dateLowest=date,
            store_id=storeID,
            is_active=True
        )
        product_new.save()

        connector_new = Connector.objects.create(
            product_id=product_new.id,
            user_id=user_id,
            is_active=True
        )
        connector_new.save()

        return Response({'message': 'success'}, status=status.HTTP_201_CREATED)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        # set product inactive
        product = self.get_object()
        product.is_active = False
        product.save()

        # set connector inactive
        productID_str = str(product.id)
        productID = int(productID_str)

        connector = Connector.objects.filter(product_id=productID)
        connector.update(is_active=False)
        for conn in connector:
            conn.save()

        return Response({"Message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


#
#   ###########   ###########   ####     ##   ###      ##   ###########   ###########   ###########   ###########   ###########
#   ##            ##        #   ## ##    ##   ## ##    ##   ##            ##                 ##       ##        #   ##        #
#   ##            ##        #   ##  ##   ##   ##  ##   ##   ###########   ##                 ##       ##        #   ###########
#   ##            ##        #   ##   ##  ##   ##   ##  ##   ##            ##                 ##       ##        #   ##    #
#   ##            ##        #   ##    ## ##   ##    ## ##   ##            ##                 ##       ##        #   ##     #
#   ###########   ###########   ##      ###   ##      ###   ###########   ###########        ##       ###########   ##      #
#


class ConnectorViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectorSerializer

    def get_queryset(self):
        """
        Return list of active connectors for signed in user
        :return:
        """
        user_id = self.request.user.id
        connectors = Connector.objects.filter(user_id=user_id, is_active=True)

        return connectors

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = ConnectorSerializer(queryset, many=True)
        return Response(serializer.data)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        # set connector inactive
        connector = self.get_object()
        connector.is_active = False
        connector.save()

        # set product inactive
        productID_id_str = str(connector.product_id)
        product_id = int(productID_id_str)

        product = Product.objects.filter(id=product_id)
        product.update(is_active=False)
        for prod in product:
            prod.save()

        return Response({"Message": "Connector deleted"}, status=status.HTTP_204_NO_CONTENT)
