from django.db import models
from django.utils import timezone
import json
from django.core.exceptions import ValidationError


class Case(models.Model):
    """
    A case represents a single inspection process/run. It can contain multiple images and multiple inspection results but
    relates to a single inspection object. So for example if you are inspecting batches of screws you would create
    one case for each batch and generate multiple images and inspection results for each case.
    """

    open_datetime = models.DateTimeField(editable=False, blank=True, null=True)
    close_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "case"

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if self.pk is None:
            self.open_datetime = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Case {self.id} opened on {self.open_datetime}"


def get_image_path(instance, filename):
    """
    Specify a dynamic path for uploaded images.
    Args:
        instance: ImageField instance
        filename: name of the uploaded file

    Returns: path to the uploaded file

    """
    return f"all/{instance.case.id}/{filename}"


class Image(models.Model):
    """
    An image captured during an inspection process. This is the main artifact that is actually inspected for defects
    so it is actually a proxy for the object being inspected.
    """

    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="images", blank=True, null=True
    )
    capture_datetime = models.DateTimeField()
    file = models.ImageField(upload_to=get_image_path)

    class Meta:
        db_table = "image"

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        """
        Delete the file from the storage when the object is deleted
        """
        self.file.delete()
        super().delete(*args, **kwargs)


# We use a new model to store the inference results. This allows for a more flexible and scalable design, as we can
# store multiple results for the same image and add more fields to the result in the future if needed.
# This also improves the separation of concerns, as the inference results are now stored in a separate table.
# Depending on the business logic, we could also consider storing the results in the image model itself, or if anomalies
# are complex enough, we could create a separate model for them and link them to the inference result.
class InferenceResult(models.Model):
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="inference_results"
    )
    anomaly_detected = models.BooleanField()
    confidence = models.FloatField()
    anomalies = (
        models.TextField()
    )  # Could also consider JSONField for direct JSON storage

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inference_result"

    def __str__(self):
        return f"Inference result for {self.image.file.name} - Anomaly Detected: {self.anomaly_detected}"

    def clean(self):
        """
        Custom validation to ensure anomalies are within the allowed list.
        """
        allowed_anomalies = ["crack", "rust"]
        if isinstance(self.anomalies, str):
            anomalies_list = json.loads(self.anomalies)
        else:
            anomalies_list = self.anomalies

        for anomaly in anomalies_list:
            if anomaly not in allowed_anomalies:
                raise ValidationError(
                    f"Anomaly '{anomaly}' is not allowed. Allowed anomalies are: {allowed_anomalies}."
                )

    def save(self, *args, **kwargs):
        """
        Overriding save to include clean method for validation.
        """
        self.clean()
        if isinstance(
            self.anomalies, list
        ):  # Ensuring anomalies are stored as a JSON string
            self.anomalies = json.dumps(self.anomalies)
        super().save(*args, **kwargs)

    def get_anomalies_list(self):
        """
        Helper method to get anomalies as a Python list.
        """
        if isinstance(self.anomalies, str):
            return json.loads(self.anomalies)
        return self.anomalies
