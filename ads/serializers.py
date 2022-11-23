from rest_framework import serializers

from ads.models import Ad


class AdListSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field="username"
    # )
    # category = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field="name"
    # )

    class Meta:
        model = Ad
        fields = '__all__'


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]