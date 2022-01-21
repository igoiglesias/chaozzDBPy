import hashlib
from pathlib import Path
from typing import List


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

    def run(self, query):
        if query['action'] == 'select':
            return self.select(query)

        if query['action'] == 'insert':
            return self.insert(query)

        if query['action'] == 'update':
            return self.update(query)

        if query['action'] == 'delete':
            return self.delete(query)

    def password(self, unhashed_password: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha1", unhashed_password.encode(), self.__salt.encode(), 100000
        ).hex()

    # Statements
    def select(self, query: list):
        pass

    def delete(self, query: list):
        table = query[1]
        conditions = "".join(query[3:]).split("=")
        db_filename = self.__location + table + self.__extension
        db_file = open(db_filename, "r")

    def insert(self, query):
        table: str = query['table_name']
        table_path: str = self.__location + table + self.__extension

        try:
            for line in query['data']:
                row = ''

                for item in line:
                    row += item + '\t'

                id: str = self.get_new_id(table_path)
                line: str = id + row + '\n'
                self.write_to_file(table_path, line, "INSERT")

                return 0
        except:
            return self.error("INSERT", "Could not insert data")

    def update(self, query: list):
        pass

    # TODO: recheck
    def error(self, query_action: str, error: str) -> bool or 0 or list:
        self.__last_error = error
        actions_allowed = ["SELECT", "INSERT", "DELETE", "UPDATE"]

        if not query_action in actions_allowed:
            return False

        if query_action == "SELECT":
            return []

        elif query_action == "INSERT":
            return 0

        else:
            return False

    def query(self, query: str):

        self.__last_error = ""

        if not query:
            return self.error("", "Empty query")

        query_sliced = query.split()
        query_action = query_sliced.pop(0)
        query_body = [item.strip() for item in query_sliced]

        self.handle_query_action(query_action, query_body)

    def handle_query_action(self, query_action: str, query: list):
        allowed_actions = ["SELECT", "DELETE", "INSERT", "UPDATE"]
        if not query_action in allowed_actions:
            return self.error(query_action, "Query not allowed")

        if query_action == "SELECT":
            self.query_select(query)
        elif query_action == "DELETE":
            self.query_delete(query)
        elif query_action == "INSERT":
            self.insert(query)
        else:
            self.query_update(query)

    def process_query_before_insert(self, query: list) -> tuple:
        query.pop(query.index("INTO"))
        remain_query: str = "".join(query)
        query_atributes: list = remain_query.split("VALUES")
        char_to_strip: list = ["(", ")"]

        columns: str = self.replace_char_from_list(
            query_atributes[0], char_to_strip)
        columns_splited: list = columns.split(",")
        values: str = self.replace_char_from_list(
            query_atributes[1], char_to_strip)
        values_splited: list = values.split(",")

        # TODO: Find a better way to do this
        data: tuple = tuple(zip(columns_splited, values_splited))

        return data

    def replace_char_from_list(self, replace_in: str, to_replace: list, replace_for: str = "") -> str:
        for item in to_replace:
            replace_in = replace_in.replace(item, replace_for)

        return replace_in

    def write_to_file(self, table_path: str, data: str, action: str):
        parameter: str = self.get_parameter(action)

        with open(table_path, parameter) as table:
            table.write(data)

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

    def format_data(self, data: tuple, write_header: bool = False) -> str:
        line: str = ""
        item_index: int = 1 if not write_header else 0

        for item in data:
            line += item[item_index] + "\t"
        line += "\n"

        return line

    def get_parameter(self, action: str) -> str:
        if action == "INSERT":
            return "a"
        else:
            return "r"

    def create_table_if_not_exist(self, table_path: str, data: tuple):
        path: object = Path(table_path)
        if not path.exists():
            header: str = self.format_data(data, write_header=True)
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
