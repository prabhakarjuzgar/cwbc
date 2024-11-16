from rest_framework import serializers
from .models import Player, PlaySession


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'division', 'secondary_division']
        read_only_fields = ['id']
        id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.division = validated_data.get('division')
        instance.secondary_division = validated_data.get('secondary_division')
        instance.name = validated_data.get('name')

        instance.save()
        return instance

    def validate(self, data):
        division = data.get('division')
        secondary_division = data.get('secondary_division')

        if secondary_division is not None:
            if secondary_division >= division:
                raise serializers.ValidationError(
                    "Secondary division must be less than the primary division."
                )

        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaySession
        fields = ['id', 'data']
        read_only_fields = ['id']
        id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return PlaySession.objects.create(**validated_data)
