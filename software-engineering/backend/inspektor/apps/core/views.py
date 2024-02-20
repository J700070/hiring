from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
import json
import logging
import sys

from inspektor.apps.core import models, serializers
from inspektor.apps.ml.tasks import run_inference_on_image


class IdInFilter(filters.FilterSet):
    """
    Filter that allows filtering by a list of IDs.
    """

    id = filters.BaseInFilter(field_name="id")

    class Meta:
        fields = ["id"]


class ModelViewSetWithIds(viewsets.ModelViewSet):
    """
    A base viewset that allows reading (and enables filtering objects by ids), creating and updating objects.
    """

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IdInFilter
    permission_classes = ()


class CaseViewSet(ModelViewSetWithIds):
    queryset = models.Case.objects.all()
    serializer_class = serializers.CaseSerializer
    model_class = models.Case


@extend_schema_view(
    create=extend_schema(request={"multipart/form-data": serializers.ImageSerializer})
)
class ImageViewSet(ModelViewSetWithIds):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    model_class = models.Image

    def perform_create(self, serializer):
        image = serializer.save()

        # Attempt to run inference on the image
        inference_result_data = run_inference_on_image(image)

        # Check if the inference was successful
        if "error" not in inference_result_data:
            # Convert anomalies list to JSON
            anomalies_json = json.dumps(inference_result_data.get("anomalies", []))

            # Create and save the InferenceResult instance
            models.InferenceResult.objects.create(
                image=image,
                anomaly_detected=inference_result_data["anomaly_detected"],
                confidence=inference_result_data["confidence"],
                anomalies=anomalies_json,
            )
        else:
            # Basic temporary logging of errors (should be improved)
            logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

            logging.error(
                f"Error processing image {image.id}: {inference_result_data['error']}"
            )
            # Handle the error here based on the business requirements
            # Some ideas might include marking the image for review, deleting the image, or simply returning the error.
            # I leave it blank for now.
