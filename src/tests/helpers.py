from unittest.mock import create_autospec

def mock_field(fieldType, return_value):
  f = create_autospec(fieldType)
  f.data = return_value
  return f
