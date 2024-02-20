from inspektor.apps.core import models
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class CaseSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Image.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = models.Case
        fields = "__all__"


class InferenceResultSerializer(serializers.ModelSerializer):
    anomalies = serializers.SerializerMethodField()

    class Meta:
        model = models.InferenceResult
        fields = [
            "anomaly_detected",
            "confidence",
            "anomalies",
            "created_at",
            "updated_at",
        ]

    def get_anomalies(self, obj):
        return obj.get_anomalies_list()


class ImageSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(
        queryset=models.Case.objects.all(), required=False, allow_null=True
    )
    file = serializers.models.ImageField()
    latest_inference_result = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = "__all__"
        parser_classes = [MultiPartParser]

    # Use extend_schema_field to explicitly define the return type for OpenAPI
    # Use OpenApiTypes.OBJECT for complex/nested objects
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_latest_inference_result(self, obj):
        # Fetches the latest related inference result, but depending on the use case, we could return all.
        latest_result = (
            models.InferenceResult.objects.filter(image=obj)
            .order_by("-created_at")
            .first()
        )
        if latest_result:
            return InferenceResultSerializer(latest_result).data
        return None
