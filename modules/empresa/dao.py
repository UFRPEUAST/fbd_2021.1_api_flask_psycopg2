from modules.shared.endereco.dao import EnderecoDao
NAME_TABLE_SQL = "EMPRESA"
_SCRIPT_SQL_INSERT = 'INSERT INTO EMPRESA(nome, cnpj) values(%s, %s) returning id'
_SCRIPT_SQL_SELECT = 'SELECT * FROM EMPRESA'
_SCRIPT_SQL_SELECT_BY_ID = 'SELECT * FROM EMPRESA WHERE ID={}'
_SCRIPT_SQL_UPDATE_BY_ID = 'UPDATE EMPRESA SET {} WHERE ID={}'


class EmpresaDao:
    def __init__(self, database):
        self.database = database
        self.dao_endereco = EnderecoDao(database=database)

    def save(self, empresa):
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_INSERT, empresa.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        empresa.set_id(id)
        return empresa

    def edit(self, id, data_empresa):
        cursor = self.database.connect.cursor()
        str = []
        for key in data_empresa.keys():
            str.append('{}=%s'.format(key))
        cursor.execute(_SCRIPT_SQL_UPDATE_BY_ID.format(','.join(str), id), list(data_empresa.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        empresas = self._get_all_or_by_id(_SCRIPT_SQL_SELECT_BY_ID.format(id))
        if empresas:
            return empresas[0]
        return None

    def get_all(self):
        empresas = self._get_all_or_by_id(_SCRIPT_SQL_SELECT)
        return empresas

    def _get_all_or_by_id(self, script):
        empresas = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        empresa_cursor = cursor.fetchone()
        while empresa_cursor:
            empresa = dict(zip(columns_name, empresa_cursor))
            empresa_cursor = cursor.fetchone()
            endereco = self.dao_endereco.get_endereco_by_empresa_id(empresa.get('id'))
            if endereco:
                endereco.pop('empresa_id')
            empresa['endereco'] = endereco
            empresas.append(empresa)
        cursor.close()
        return empresas
