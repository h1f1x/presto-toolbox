from configparser import ConfigParser
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from presto import query

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.mark.integration_test
def test_example_config_db_and_query_should_work():
    """
    Test that the example config contains db fields which are required for the db connection.
    Populating the example config DB section with all required fields from the real config
    """
    example_config = ConfigParser()
    example_config.read(f"{__location__}/../config.ini.example")

    real_config = ConfigParser()
    real_config.read(f"{__location__}/../config.ini")

    for db_field in example_config["DB"]:
        assert db_field in real_config["DB"], "DB field is missing in real config"
        example_config["DB"][db_field] = real_config["DB"][db_field]

    query.query(example_config["DB"], "SELECT 1")
