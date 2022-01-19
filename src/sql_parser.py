def sql_parser(sql):
    mid_lang = {}

    if 'INSERT' in sql:
        import re

        data = []
        regex = r"\((.*?)\)"

        splited = sql.split(' ')
        table_name = splited[2]

        between_parentheses = re.findall(regex, sql, re.MULTILINE)
        columns = between_parentheses[0].split(',')

        for idx, item in enumerate(between_parentheses):
            if idx != 0:
                el = []
                item_splited = item.split(',')

                for i in item_splited:
                    el.append(i.replace('"', '') + '\t')

                data.append(el)

        mid_lang['action'] = 'insert'
        mid_lang['columns'] = columns
        mid_lang['data'] = data
        mid_lang['table_name'] = table_name

        return mid_lang

    if 'SELECT' in sql:
        query_splited = sql.split(' ')
        table_name = query_splited[query_splited.index('FROM') + 1]

        mid_lang['action'] = 'select'
        mid_lang['table_name'] = table_name

        if '*' in query_splited:
            mid_lang['columns'] = '*'
            return mid_lang

        import re
        regex = r"\((.*?)\)"
        columns = re.findall(regex, sql, re.MULTILINE)

        mid_lang['columns'] = columns[0].split(',')
        id = query_splited.index('WHERE')

        if id < 0:
            raise Exception("Id cannot be 0 or negative")

        # FIX: tem forma melhor de pegar o id
        mid_lang['where'] = {'id': query_splited[id + 3]}

        return mid_lang

    if 'UPDATE' in sql:

        query_splited = sql.split(' ')
        table_name = query_splited[1]

        # FIX: tem forma melhor de pegar o id
        id = query_splited.index('WHERE')

        if id < 0:
            raise Exception("Id cannot be 0 or negative")

        # FIX: tem forma melhor de pegar o id
        set_stmt_position = query_splited.index('SET')
        column = query_splited[set_stmt_position + 1]
        value = query_splited[set_stmt_position + 3]

        mid_lang['action'] = 'delete'
        mid_lang['action'] = 'update'
        mid_lang['table_name'] = table_name
        mid_lang['data'] = {'data': {column: value.replace('"', '')}}
        mid_lang['where'] = {'id': query_splited[id + 3]}

        return mid_lang

    if 'DELETE' in sql:
        query_splited = sql.split(' ')
        table_name = query_splited[query_splited.index('FROM') + 1]

        mid_lang['action'] = 'select'
        mid_lang['table_name'] = table_name

        id = query_splited.index('WHERE')

        if id < 0:
            raise Exception("Id cannot be 0 or negative")

        mid_lang['action'] = 'delete'
        # FIX: tem forma melhor de pegar o id
        mid_lang['where'] = {'id': query_splited[id + 3]}
        return mid_lang


# INSERT
parsed_query = sql_parser('INSERT into users (nome, idade, sexo) values ("fulano", "21", "M"), ("ciclana", "22", "F")')

# SELECT
# parsed_query = sql_parser('SELECT * FROM users')
# parsed_query = sql_parser('SELECT (id, name) FROM users WHERE id = 1')

# UPDATE
# parsed_query = sql_parser('UPDATE users SET name = "fulano" WHERE id = 1')

# DELETE
# parsed_query = sql_parser('DELETE FROM users WHERE id = 1')

print(parsed_query)
