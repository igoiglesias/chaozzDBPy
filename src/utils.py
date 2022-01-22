import re


class SqlParser:
    def parser(self, sql: str) -> dict:
        mid_lang: dict = {}

        if "INSERT" in sql:

            data: list = []
            regex = r"\((.*?)\)"

            sql_splited: list = sql.split(" ")
            table_name: str = sql_splited[2]

            between_parentheses: list = re.findall(regex, sql, re.MULTILINE)
            columns: list = between_parentheses[0].split(",")

            for idx, item in enumerate(between_parentheses):
                if idx != 0:
                    el: list = []
                    item_splited: list = item.split(",")

                    for i in item_splited:
                        # el.append(i.replace('"', '') + '\t')
                        el.append(i.replace('"', ""))

                    data.append(el)

            mid_lang["action"] = "insert"
            mid_lang["columns"] = columns
            mid_lang["data"] = data
            mid_lang["table_name"] = table_name

            return mid_lang

        if "SELECT" in sql:
            query_splited = sql.split(" ")
            table_name = query_splited[query_splited.index("FROM") + 1]

            mid_lang["action"] = "select"
            mid_lang["table_name"] = table_name

            if "*" in query_splited:
                mid_lang["columns"] = "*"
                return mid_lang

            regex = r"\((.*?)\)"
            columns = re.findall(regex, sql, re.MULTILINE)

            mid_lang["columns"] = columns[0].split(",")
            id = query_splited.index("WHERE")

            if id < 0:
                raise Exception("Id cannot be 0 or negative")

            # FIX: tem forma melhor de pegar o id
            mid_lang["where"] = {"id": query_splited[id + 3]}

            return mid_lang

        if "UPDATE" in sql:

            query_splited = sql.split(" ")
            table_name = query_splited[1]

            # FIX: tem forma melhor de pegar o id
            id = query_splited.index("WHERE")

            if id < 0:
                raise Exception("Id cannot be 0 or negative")

            # FIX: tem forma melhor de pegar o id
            set_stmt_position = query_splited.index("SET")
            column = query_splited[set_stmt_position + 1]
            value = query_splited[set_stmt_position + 3]

            mid_lang["action"] = "delete"
            mid_lang["action"] = "update"
            mid_lang["table_name"] = table_name
            mid_lang["data"] = {"data": {column: value.replace('"', "")}}
            mid_lang["where"] = {"id": query_splited[id + 3]}

            return mid_lang

        if "DELETE" in sql:
            query_splited = sql.split(" ")
            table_name = query_splited[query_splited.index("FROM") + 1]

            mid_lang["action"] = "select"
            mid_lang["table_name"] = table_name

            id = query_splited.index("WHERE")

            if id < 0:
                raise Exception("Id cannot be 0 or negative")

            mid_lang["action"] = "delete"
            # FIX: tem forma melhor de pegar o id
            mid_lang["where"] = {"id": query_splited[id + 3]}

            return mid_lang
