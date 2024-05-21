from abc import ABC, abstractmethod

class Transformation(ABC):
    """
    Transformation base class
    """

    def type(self, type: str):
        self.type = type

    @abstractmethod
    def transform(self, data: dict):
        raise NotImplementedError(f"Transformation for {self.type} not implemented")
    
# Other notification types can be implemented just like this with business logic in transform function
class NoTransformation(Transformation):
    """
    Does nothing, returns the data
    """
    def transform(self, data: dict):
        return data
    
# Maps notification types with class which does the transformation
TRANSFORMS = {
    "send_all_data": NoTransformation,
    # Implement other classes for other types
}