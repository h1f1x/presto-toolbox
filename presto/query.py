import os
from configparser import ConfigParser
from contextlib import contextmanager
from typing import Any, Dict

import prestodb
import urllib3
from codetiming import Timer
from prestodb.client import PrestoResult
from prestodb.dbapi import Connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_config() -> ConfigParser:
    config = ConfigParser()
    config.read("config.ini")
    if not "user" in config["DB"]:
        config["DB"]["user"] = os.getenv("USER", "presto-toolbox")
    return config


@contextmanager
def db_connect(db: Dict[str, Any]) -> Connection:
    with prestodb.dbapi.connect(
        host=db["host"],
        port=db["port"],
        user=db["user"],
        catalog=db["catalog"],
        schema=db["schema"],
        http_scheme=db["http_scheme"],
    ) as conn:
        # optinionated by default unsecure but often needed
        conn._http_session.verify = False
        yield conn


def query(db_config: ConfigParser, query_string: str) -> PrestoResult:
    with db_connect(db_config) as conn:
        cur = conn.cursor()
        for row in cur.execute(query_string):
            yield row


def query_string(config: ConfigParser, query_name: str) -> str:
    return config[f"Query.{query_name}"]["query"]


def show_query_result(config: ConfigParser, query_name: str) -> None:
    return config.has_option(f"Query.{query_name}", "show_result")


if __name__ == "__main__":
    config = read_config()
    with Timer(name="context manager"):
        query_name = "foo"
        print(f"Querying {query_name}...")
        print(query_string(config, query_name))
        result = query(config["DB"], query_string(config, query_name))
        c = 0
        for row in result:
            c += 1
            if show_query_result(config, query_name):
                print(row)
            else:
                if c % 100000 == 0:
                    print(f"Fetched until now {c} rows.")
        print(f"Total fetched {c} rows.")
