from abc import ABC, abstractmethod
import random

class BaseAIDriver(ABC):
    @abstractmethod
    def predict(self, data):
        pass

class MockAIDriver(BaseAIDriver):
    def predict(self, data):
        # Default mock behavior: Return a confidence score and a mock result
        confidence = round(random.uniform(0.7, 0.99), 2)
        return {
            "confidence": confidence,
            "status": "PASS" if confidence > 0.8 else "FAIL",
            "metadata": {"source": "mock_engine"}
        }

# Provision for adding real ML models (e.g., DeepFace, EasyOCR)
# class RealAIDriver(BaseAIDriver): ...
