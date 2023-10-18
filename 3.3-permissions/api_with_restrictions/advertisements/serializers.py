from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id',
                  'title',
                  'description',
                  'creator',
                  'status',
                  'created_at',
                  )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # Обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # Само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user_open = Advertisement.objects.filter(creator=self.context["request"].user, status="OPEN").count()
        if self.context["request"].method == 'POST' and user_open >= 10:
            raise serializers.ValidationError('Exceed max advertisement count with status = OPEN')

        if self.context["request"].method == 'PATCH' and user_open >= 10 and data.get('status') == 'OPEN':
            raise serializers.ValidationError(f'Ограничение для пользователя {user_open} 10 элем/мин!')

        return data
