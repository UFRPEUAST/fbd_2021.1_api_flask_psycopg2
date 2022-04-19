from modules.shared.endereco.dao import EnderecoDao

_SCRIPT_SQL_INSERT = 'INSERT INTO EMPRESA(nome, cnpj) values(%s, %s) returning id'
_SCRIPT_SQL_SELECT = 'SELECT * FROM EMPRESA'


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

    def edit(self, empresa):
        print('Já vai existir o id')

    def get_by_id(self, id):
        print('BUSCAR NO BANCO PARA SABER SE EXISTE UMA EMPRESA COM ESSE ID')

    def get_all(self):
        empresas = []
        cursor = self.database.connect.cursor()
        cursor.execute(_SCRIPT_SQL_SELECT)
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
