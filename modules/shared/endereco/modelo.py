

class Endereco:
    VALIDATE_FIELDS_REQUIREMENTS = ['cep', 'rua', 'bairro', 'numero', 'cidade', 'estado']
    def __init__(self, cep, rua, bairro, numero, cidade, estado):
        self.id = None
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.cidade = cidade
        self.estado = estado

    def set_id(self, id):
        self.id = id

    def get_values_save(self, empresa_id):
        return [self.cep, self.rua, self.bairro, self.numero, self.cidade, self.estado, empresa_id]

    def __str__(self):
        return 'Rua: {} - Nº: {} Bairro: {} - Cidade: {} - {} CEP:{}'.format(self.rua, self.numero, self.bairro, self.cidade, self.estado, self.cep)
