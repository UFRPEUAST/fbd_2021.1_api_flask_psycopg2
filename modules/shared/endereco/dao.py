_SCRIPT_SQL_INSERT = 'INSERT INTO ENDERECO(cep, rua, bairro, numero, cidade, estado, empresa_id) values(%s, %s, %s, %s, %s, %s, %s) returning id'
_SCRIPT_SQL_SELECT_ALL = 'SELECT * FROM ENDERECO'
_SCRIPT_SQL_SELECT_BY_ID_EMPRESA = 'SELECT * FROM ENDERECO where empresa_id={}'


class EnderecoDao:
    def __init__(self, database):
        self.database = database

    def save(self, endereco, empresa_id):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, endereco.get_values_save(empresa_id))
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        endereco.set_id(id)
        return endereco

    def get_endereco_by_empresa_id(self, empresa_id):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_SELECT_BY_ID_EMPRESA.format(empresa_id))
        columns_name = [column[0] for column in cursor.description]
        endereco = cursor.fetchone()
        print('**************', endereco)
        if endereco:
            endereco = dict(zip(columns_name, endereco))
        cursor.close()
        return endereco

    # def get_all(self):
    #     empresas = []
    #     cursor = self.database.connect.cursor()
    #     cursor.execute(_SCRIPT_SQL_SELECT)
    #     columns_name = [column[0] for column in cursor.description]
    #     empresa_cursor = cursor.fetchone()
    #     while empresa_cursor:
    #         empresa = dict(zip(columns_name, empresa_cursor))
    #         empresa_cursor = cursor.fetchone()
    #         empresas.append(empresa)
    #     cursor.close()
    #     return empresas
