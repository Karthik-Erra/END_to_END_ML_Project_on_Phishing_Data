from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file


file = read_yaml_file(SCHEMA_FILE_PATH)
number_of_columns = len(file.get("columns","no_columns"))

print(file.get("numerical_columns"))

print(type(file.get("numerical_columns")))