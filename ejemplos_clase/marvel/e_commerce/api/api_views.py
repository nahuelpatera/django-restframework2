# Primero, importamos los serializadores
from e_commerce.api.serializers import *

# Segundo, importamos los modelos:
from django.contrib.auth.models import User
from e_commerce.models import Comic,WishList

# Luego importamos las herramientas para crear las api views con Django REST FRAMEWORK:

# (GET) Listar todos los elementos en la entidad:
from rest_framework.generics import ListAPIView

# (POST) Inserta elementos en la DB
from rest_framework.generics import CreateAPIView

# (GET-POST) Para ver e insertar elementos en la DB
from rest_framework.generics import ListCreateAPIView

from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.generics import DestroyAPIView

# Esto en realidad lo podemos hacer como:
# from rest_framework.generics import (
#     ListAPIView,
#     CreateAPIView,
#     ListCreateAPIView,
#     RetrieveUpdateAPIView,
#     DestroyAPIView)
# de manera más prolija

# Importamos librerías para gestionar los permisos de acceso a nuestras APIs
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

# NOTE: Importamos este decorador para poder customizar los 
# parámetros y responses en Swagger, para aquellas
# vistas de API basadas en funciones y basadas en Clases 
# que no tengan definido por defecto los métodos HTTP.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


mensaje_headder = '''
Ejemplo de header:

`headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  'actions': 'PUT',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}`
'''
# NOTE: APIs genéricas:

class GetComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro, o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# NOTE: APIs MIXTAS:

class GetOneComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        '''
        Sobrescribimos la función `get_queryset` para poder filtrar el request 
        por medio de la url. En este caso traemos de la url por medio de `self.kwargs` 
        el parámetro `comic_id` y con él realizamos una query para traer 
        el comic del ID solicitado.  
        '''
        try:
            comic_id = self.kwargs['comic_id']
            queryset = Comic.objects.filter(id=comic_id)
            return queryset
        except Exception as error:
            return {'error': f'Ha ocurrido la siguiente excepción: {error}'}

class LoginUserAPIView(APIView):
    '''
    ```
    Vista de API personalizada para recibir peticiones de tipo POST.
    Esquema de entrada:
    {"username":"root", "password":12345}
    
    Utilizaremos JSONParser para tener  'Content-Type': 'application/json'\n\n
    Esta función sobrescribe la función post original de esta clase,
    recibe "request" y hay que setear format=None, para poder recibir 
    los datos en "request.data", la idea es obtener los datos enviados en el 
    request y autenticar al usuario con la función "authenticate()", 
    la cual devuelve el estado de autenticación.
    Luego con estos datos se consulta el Token generado para el usuario,
    si no lo tiene asignado, se crea automáticamente.
    Esquema de entrada:\n
    {
        "username": "root",
        "password": 12345
    }
    ```
    '''
    parser_classes = [JSONParser]
    # renderer_classes = [JSONRenderer]
    authentication_classes = []
    permission_classes = []

    # NOTE: Agregamos todo esto para personalizar
    # el body de la request y los responses
    # que muestra como ejemplo el Swagger para
    # este método.

    # NOTE 2: Descomentar dicho decorador para
    # mostrarlo en clase.

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT, 
    #         properties={
    #             'username': openapi.Schema(
    #                 type=openapi.TYPE_STRING,
    #                 description='username'
    #             ),
    #             'password': openapi.Schema(
    #                 type=openapi.TYPE_STRING,
    #                 format=openapi.FORMAT_PASSWORD,
    #                 description='password'
    #             ),
    #         }
    #     ),
    #     responses= {
    #         "201": openapi.Response(
    #             description='Return Token',
    #             examples={
    #                 "application/json": {
    #                     "user_id": 1,
    #                     "username": "username",
    #                     "first_name": "first_name",
    #                     "last_name": "last_name",
    #                     "email": "email@email.com",
    #                     "is_active": True,
    #                     "token": "92937874f377a1ea17f7637ee07208622e5cb5e6"
    #                 }
    #             }
    #         ),
    #        "400": openapi.Response(
    #             description='Credenciales Inválidas',
    #             examples={
    #                 "application/json": {
    #                     'response': 'Error',
    #                     'error_message': 'Credenciales invalidas'
    #                 }
    #             }
    #         ),
    #     }
    # )
    def post(self, request):
        user_data = {}
        try:
            # Obtenemos los datos del request:
            username = request.data.get('username')
            password = request.data.get('password')
            # Obtenemos el objeto del modelo user, a partir del usuario y contraseña,
            # NOTE: es importante el uso de este método, porque aplica el hash del password!
            account = authenticate(username=username, password=password)

            if account:
                # Si el usuario existe y sus credenciales son validas, tratamos de obtener el TOKEN:
                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    # Si el TOKEN del usuario no existe, lo creamos automáticamente:
                    token = Token.objects.create(user=account)
                # Con todos estos datos, construimos un JSON de respuesta:
                user_data['user_id'] = account.pk
                user_data['username'] = username
                user_data['first_name'] = account.first_name
                user_data['last_name'] = account.first_name
                user_data['email']=account.email
                user_data['is_active'] = account.is_active
                user_data['token'] = token.key                
                # Devolvemos la respuesta personalizada
                return Response(
                    data=user_data, status=status.HTTP_201_CREATED
                )
            else:
                # Si las credenciales son invalidas, devolvemos algun mensaje de error:
                user_data['response'] = 'Error'
                user_data['error_message'] = 'Credenciales invalidas'
                return Response(
                    data=user_data, status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as error:
            # Si aparece alguna excepción, devolvemos un mensaje de error
            user_data['response'] = 'Error'
            user_data['error_message'] = error
            return Response(
                data=user_data, status=status.HTTP_400_BAD_REQUEST
            )

# TODO: Agregar las vistas genericas que permitan realizar un CRUD del modelo de wish-list.
# TODO: Crear una vista generica modificada para traer todos los comics que tiene un usuario.