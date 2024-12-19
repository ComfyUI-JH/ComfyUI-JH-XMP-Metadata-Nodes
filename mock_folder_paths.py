import sys
from unittest.mock import Mock

pytest_plugins = []  # Empty, but marks this file as a plugin

# Mock folder_paths early, before test code runs
mock_folder_paths = Mock()

# Inject into sys.modules
sys.modules["folder_paths"] = mock_folder_paths
