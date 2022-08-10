
# Primero importamos los modelos que queremos serializar:
from e_commerce.models import Comic, WishList
from django.contrib.auth.models import User

# Luego importamos todos los serializadores de django rest framework.
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class ComicSerializer(serializers.ModelSerializer):
    # new_field =  serializers.SerializerMethodField()
    
    class Meta:
        model = Comic
        fields = ('marvel_id','title', 'description', 'price', 'stock_qty', 'picture')
        # fields = ('marvel_id', 'title', 'algo')

    # def get_new_field(self, obj):
    #     return {'hola':10}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        _username = self.Meta.model.objects.filter(
            username=data.get('username')
        ).first()
        if not _username:
            raise serializers.ValidationError(
                'El username ingresado no existe'
            )
        if not _username.check_password(data.get('password')):
            raise serializers.ValidationError(
                'La password ingresada es incorrecta'
            )
        return data

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user')
        

# TODO: Realizar el serializador para el modelo de WishList