_SCRIPT_SQL_INSERT = 'INSERT INTO EMPRESA(nome, cnpj) values(%s, %s) returning id'
_SCRIPT_SQL_SELECT = 'SELECT * FROM EMPRESA'


class EmpresaDao:
    def __init__(self, database):
        self.database = database

    def save(self, empresa):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, empresa.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        empresa.set_id(id)
        return empresa

    def get_all(self):
        empresas = []
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_SELECT)
        columns_name = [column[0] for column in cursor.description]
        empresa_cursor = cursor.fetchone()
        while empresa_cursor:
            empresa = dict(zip(columns_name, empresa_cursor))
            empresa_cursor = cursor.fetchone()
            empresas.append(empresa)
        cursor.close()
        return empresas
