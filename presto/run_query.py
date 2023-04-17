import os
from configparser import ConfigParser, SectionProxy
from contextlib import contextmanager
from typing import Any, Dict

import prestodb
import urllib3

from prestodb.client import PrestoResult
from prestodb.dbapi import Connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore


def read_config(config_file: str) -> ConfigParser:
    config = ConfigParser()
    config.read(config_file)
    print(f"[] Read config from {config_file}")
    if not "user" in config["DB"]:
        config["DB"]["user"] = os.getenv("USER", "presto-toolbox")
    return config


@contextmanager
def db_connect(db: SectionProxy) -> Connection:
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


def execute(db_config: SectionProxy, query_string: str) -> PrestoResult:
    with db_connect(db_config) as conn:
        cur = conn.cursor()
        for row in cur.execute(query_string):
            yield row


def query_one(db_config: SectionProxy, query_string: str) -> PrestoResult:
    with db_connect(db_config) as conn:
        cur = conn.cursor()
        cur.execute(query_string)
        return cur.fetchone()


def query_string(config: ConfigParser, query_name: str) -> str:
    return config[f"Query.{query_name}"]["query"]


def show_query_result(config: ConfigParser, query_name: str) -> bool:
    return not config.has_option(f"Query.{query_name}", "hide-result")


if __name__ == "__main__":
    pass
