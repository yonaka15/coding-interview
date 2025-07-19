import unicodedata

from rest_framework import serializers

from api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        if value:
            # Convert full-width to half-width characters
            value = unicodedata.normalize('NFKC', value)
            # Strip whitespace
            value = value.strip()
        return value