import sys
from unittest.mock import Mock

# Mock folder_paths early, before test code runs
mock_folder_paths = Mock()

# Inject into sys.modules
sys.modules["folder_paths"] = mock_folder_paths
