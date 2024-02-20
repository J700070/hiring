from inspektor.apps.core.models import Image
import random
import logging
import sys


def analyze_image(image):
    """
    Implement this function to analyze the given image.
    Args:
        image: Image

    Returns: dict

    """
    # Placeholder implementation
    return {
        "confidence": random.uniform(
            0.5, 1.0
        ),  # Mock confidence score between 0.5 and 1
        "anomalies": ["crack", "rust"]
        if random.choice([True, False])
        else [],  # Mock anomalies
    }


def run_inference_on_image(image: Image):
    """
    Implement this function to run inference on the given image.
    Args:
        image: Image

    Returns: dict

    """
    try:
        # Actual analysis logic (placeholder in this example)
        analysis_result = analyze_image(image)

        anomaly_detected = bool(analysis_result["anomalies"])

        return {
            "image_id": image.id,
            "anomaly_detected": anomaly_detected,
            "confidence": analysis_result["confidence"],
            "anomalies": analysis_result["anomalies"],
        }
    except Exception as e:
        # Basic temporary logging of errors (should be improved)
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

        logging.error(f"Error processing image {image.id}: {e}")
        return {"image_id": image.id, "error": "Failed to process image."}
