class Empresa:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.id = None

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return 'Nome: {} - CNPJ: {}'.format(self.nome, self.cnpj)

    def get_values_save(self):
        return [self.nome, self.cnpj]