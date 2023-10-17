from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# (GET - ListAPIView) Listar todos los elementos en la entidad:
# (POST - CreateAPIView) Inserta elementos en la DB
# (GET - RetrieveAPIView) Devuelve un solo elemento de la entidad.
# (GET-POST - ListCreateAPIView) Para listar o insertar elementos en la DB
# (GET-PUT - RetrieveUpdateAPIView) Devuelve o actualiza un elemento en particular.
# (DELETE - DestroyAPIView) Permite eliminar un elemento.
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
# Importamos librerías para gestionar los permisos de acceso a nuestras APIs
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication, TokenAuthentication
)
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from e_commerce.api.serializers import *
from e_commerce.models import Comic, WishList


mensaje_headder = '''
Class API View

```
headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  
  'actions': 'GET', 'POST', 'PUT', 'PATCH', 'DELETE',
  
  'Content-Type': 'application/json',
  
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}
```
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

    # Equivale a --> permission_classes = (IsAdminUser & IsAuthenticated,)
    permission_classes = (IsAuthenticated | IsAdminUser,)
    # Descomentar y mostrar en clases para ver las diferencias entre 
    # estos tipos de Authentication. Mostrar en Postman.

    # HTTP Basic Authentication
    # authentication_classes = [BasicAuthentication]

    # Token Authentication
    # authentication_classes = [TokenAuthentication]


class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos, pero en este caso ordenados según "marvel_id".
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all().order_by('marvel_id')
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


# En este caso observamos como es el proceso de actualización "parcial"
# utilizando el serializador para validar los datos que llegan del request.
# Dicho proceso se conoce como "deserialización".
class UpdateComicAPIView(UpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)
    lookup_field = 'marvel_id'

    def put(self, request, *args, **kwargs):
        _serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            many=False,
            partial=True
        )
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


# class GetOneComicAPIView(RetrieveAPIView):
#     __doc__ = f'''{mensaje_headder}
#     `[METODO GET]`
#     Esta vista de API nos devuelve un comic en particular de la base de datos.
#     '''
#     serializer_class = ComicSerializer
#     permission_classes = (IsAuthenticated | IsAdminUser,)
#     queryset = Comic.objects.all()


class GetOneComicAPIView(RetrieveAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated | IsAdminUser,)
    queryset = Comic.objects.all()

    def get_queryset(self):
        '''
        Sobrescribimos el método `get_queryset()` para poder filtrar el 
        request por medio de la url. En este caso traemos de la url 
        por medio de `self.kwargs` el parámetro `id` y con él 
        realizamos una query para traer el comic del ID solicitado. 
        '''
        comic_id = self.kwargs['pk']
        queryset = self.queryset.filter(id=comic_id)
        return queryset


class GetOneMarvelComicAPIView(RetrieveAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos
    a partir del valor del campo "marvel_id" pasado por URL.
    '''
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated | IsAdminUser,)
    queryset = Comic.objects.all()
    lookup_field = 'marvel_id'

# Otra forma de realizar un Get y traernos un solo
# # objeto o instancia(Detalle) utilizando el método ".get_object()"
# y sobreescribiendo el método ".get()".
# class GetOneMarvelComicAPIView(RetrieveAPIView):
#     serializer_class = ComicSerializer
#     permission_classes = (IsAuthenticated | IsAdminUser,)
#     queryset = Comic.objects.all()
#     lookup_field = 'marvel_id'

#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(
#             instance=self.get_object(), many=False
#         )
#         return Response(
#             data=serializer.data, status=status.HTTP_200_OK
#         )


# Si tuvieramos que hacerlo más genérico, usamos APIView, lo cual
# nos permite tener más personalización sobre la View.
# class GetOneMarvelComicAPIView(APIView):
#     permission_classes = (IsAuthenticated | IsAdminUser,)

#     def get_queryset(self):
#         return Comic.objects.filter(
#             marvel_id=self.kwargs.get('marvel_id')
#         )

#     def get(self, request, *args, **kwargs):
#         _queryset = self.get_queryset()
#         if not _queryset.exists():
#             return Response(
#                 data={'detail': 'Not found.'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ComicSerializer(
#             instance=_queryset.first(), many=False
#         )
#         return Response(
#             data=serializer.data, status=status.HTTP_200_OK
#         )


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
    parser_classes = (JSONParser,)
    # renderer_classes = [JSONRenderer]
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        # Realizamos validaciones a través del serializador
        user_login_serializer = UserLoginSerializer(data=request.data)
        if user_login_serializer.is_valid():
            _username = request.data.get('username')
            _password = request.data.get('password')

            # Si el usuario existe y sus credenciales son validas,
            # tratamos de obtener el TOKEN:
            _account = authenticate(username=_username, password=_password)
            if _account:
                _token, _created = Token.objects.get_or_create(user=_account)
                return Response(
                    data=TokenSerializer(instance=_token, many=False).data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data={'error': 'Invalid Credentials.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=user_login_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# TODO: Agregar las vistas genericas(vistas de API basadas en clases) 
# que permitan realizar un CRUD del modelo de wish-list.
# TODO: Crear una vista generica modificada(vistas de API basadas en clases)
# para traer todos los comics que tiene un usuario.


class GetWishListAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los WishList presentes 
    en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer

    # Equivale a --> permission_classes = (IsAdminUser & IsAuthenticated,)
    permission_classes = (IsAuthenticated | IsAdminUser,)
    # Descomentar y mostrar en clases para ver las diferencias entre 
    # estos tipos de Authentication. Mostrar en Postman.

    # HTTP Basic Authentication
    # authentication_classes = [BasicAuthentication]

    # Token Authentication
    # authentication_classes = [TokenAuthentication]


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)



# En este caso observamos como es el proceso de actualización "parcial"
# utilizando el serializador para validar los datos que llegan del request.
# Dicho proceso se conoce como "deserialización".
class UpdateWishListAPIView(UpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)
    lookup_field = 'comic_id'

    def put(self, request, *args, **kwargs):
        _serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            many=False,
            partial=True
        )
        sin_error = self.request.user == _serializer.get_user and self.request.comic == _serializer.get_comic 
        if _serializer.is_valid():
            if _serializer.is_valid():
                 if self.request.user != _serializer.validated_data['user'] or self.request.comic != _serializer.validated_data['comic']:
                    return Response(
                    data={'error': 'No puede modificarse el usuario o el comic'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    


class DeleteWishListAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los WishList presentes 
    en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)
    lookup_field = 'comic_id'

        
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset