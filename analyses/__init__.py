import importlib
import pkgutil
from typing import Dict

from .base_analysis import BaseAnalysis

FEATURES: Dict[int, BaseAnalysis] = {}

def discover_features():
    """
    Dynamically discovers and registers all feature classes in the analyses package.
    """
    package = importlib.import_module(__name__)
    package_path = package.__path__

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        # Skip the base_feature module
        if module_name == 'base_feature':
            continue
        
        module = importlib.import_module(f"{__name__}.{module_name}")
        
        # Iterate through attributes to find classes inheriting from BaseAnalysis
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type) 
                and issubclass(attribute, BaseAnalysis) 
                and attribute is not BaseAnalysis
            ):
                feature_instance = attribute()
                if feature_instance.feature_id in FEATURES:
                    raise ValueError(f"Duplicate feature_id {feature_instance.feature_id} in feature '{feature_instance.name()}'.")
                FEATURES[feature_instance.feature_id] = feature_instance

# Discover features upon import
discover_features()
