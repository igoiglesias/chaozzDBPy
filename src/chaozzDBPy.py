import hashlib
from pathlib import Path
from typing import Any, List

from src.utils import SqlParser


class ChaozzDBPy:
    def __init__(
        self,
        delimiter: str = "\t",
        location: str = "db/",
        extension: str = ".tsv",
        salt: str = "@Chaozz#DB!PYthon",
        max_records: int = 999,
        last_error: str = "",
    ):
        self.__delimiter = delimiter
        self.__location = location
        self.__extension = extension
        self.__salt = salt
        self.__max_records = max_records
        self.__last_error = last_error

    # TODO: Find a better algo to generate the hash
    def password(self, unhashed_password: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha1", unhashed_password.encode(), self.__salt.encode(), 100000
        ).hex()

    def run(self, sql: str):
        query: dict = SqlParser().parser(sql)

        self.__handle_query_action(query)

    def __handle_query_action(self, query: dict):
        allowed_actions = ["select", "delete", "insert", "update"]
        if not query["action"] in allowed_actions:
            return self.error(query["action"], "Query not allowed")

        if query["action"] == "select":
            return self.select(query)

        if query["action"] == "insert":
            return self.insert(query)

        if query["action"] == "update":
            return self.update(query)

        if query["action"] == "delete":
            return self.delete(query)

    def select(self, query: dict):
        pass

    def insert(self, query: dict):
        table: str = query["table_name"]
        table_path: str = self.__location + table + self.__extension

        try:
            for line in query["data"]:

                row = self.format_data(line)
                id: str = self.get_new_id(table_path)
                line: str = id + row + "\n"

                self.create_table_if_not_exist(table_path, query["columns"])
                self.write_to_file(table_path, line, "INSERT")

                return 0
        except:
            return self.error("INSERT", "Could not insert data")

    def update(self, query: dict):
        pass

    def delete(self, query: dict):
        pass

    # TODO: Find a betteer way to do this
    def error(self, query_action: str, error: str) -> Any:
        self.__last_error = error
        actions_allowed = ["SELECT", "INSERT", "DELETE", "UPDATE"]

        if query_action not in actions_allowed:
            return False

        if query_action == "SELECT":
            return []

        elif query_action == "INSERT":
            return 0

        else:
            return False

    def get_new_id(self, table_path: str) -> str:
        last_line: list = self.read_from_file(table_path, line=-1)
        # TODO: Find a better way to do this too
        id: str = last_line[0].split("\t")[0]

        try:
            id = int(id)
            id = str(id + 1)
        except:
            id = "1"

        id += "\t"

        return id

    def write_to_file(self, table_path: str, data: str, action: str):
        parameter: str = self.get_parameter(action)

        with open(table_path, parameter) as table:
            table.write(data)

    def format_data(self, data: list, is_header: bool = False) -> str:
        line: str = ""
        if is_header:
            data.insert(0, "id")

        for item in data:
            line += item + "\t"
        line += "\n"

        return line

    def get_parameter(self, action: str) -> str:
        if action == "INSERT":
            return "a"
        else:
            return "r"

    def create_table_if_not_exist(self, table_path: str, data: list):
        path: object = Path(table_path)
        if not path.exists():
            header: str = self.format_data(data, is_header=True)
            self.write_to_file(table_path, header, "INSERT")

    def read_from_file(self, table_path: str, line: int = 0) -> List[str]:
        parameter: str = "r"
        file: list = []
        lines_from_file: list = []
        try:
            with open(table_path, parameter) as table:
                file: list = table.readlines()
            if line != 0:
                lines_from_file.append(file[line])
            else:
                lines_from_file.append(file)

        except:
            lines_from_file.append("")

        return lines_from_file
