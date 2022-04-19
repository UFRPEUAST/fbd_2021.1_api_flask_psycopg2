from flask import Blueprint, request, jsonify, make_response, Response
from modules.empresa.dao import EmpresaDao
from modules.empresa.modelo import Empresa
from modules.shared.endereco.dao import EnderecoDao
from modules.shared.endereco.modelo import Endereco
from utils.database import ConnectSingletonDB
import traceback

app_empresa = Blueprint('app_empresa', __name__)
app_name = "empresa"
dao = EmpresaDao(database=ConnectSingletonDB())
dao_endereco = EnderecoDao(database=ConnectSingletonDB())


@app_empresa.route('/{}/'.format(app_name),
                   methods=['GET'])
def get_empresas():
    empresas = dao.get_all()
    print('empresas', empresas)
    return make_response(jsonify(empresas), 200)


@app_empresa.route('/{}/add/'.format(app_name),
                   methods=['POST'])
def add_empresa():
    try:
        data = request.form.to_dict(flat=True)
        empresa = None
        # Validação para existir se todos os fields (Nome e CPF)
        # existem na requisição
        VALIDATE_TEMP(data)
        empresa = Empresa(nome=data.get('nome'),
                          cnpj=data.get('cnpj'))
        empresa = dao.save(empresa)
        if data.get('cep'):
            print('OBA, vamos salvar o endereço')
            data.pop('nome')
            data.pop('cnpj')
            endereco = Endereco(**data)
            endereco = dao_endereco.save(endereco, empresa.id)
            empresa.set_end(endereco)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    return make_response({'id': empresa.id}, 201)


@app_empresa.route('/{}/<id>/'.format(app_name),
                   methods=['PUT'])
def edit_empresa(id):
    data = request.form.to_dict(flat=True)
    print('DATA', data)
    print('ID', id)
    #1 - Buscar a empresa pelo id, se existir, chama o edit
    return make_response({}, 201)

@app_empresa.route('/{}/<id>/'.format(app_name),
                   methods=['GET'])
def get_empresa_by_id(id):
    data = request.form.to_dict(flat=True)
    print('DATA', data)
    print('ID', id)
    #1 - Buscar a empresa pelo id, se existir, chama o edit
    return make_response({}, 201)


# TODO - refactory - Depois vamos remover e colocar em uma classe que terá a responsabilidade de validações
# EmpresaBusinnes
def VALIDATE_TEMP(data):
    # 1 - Primeiro, validamos se existe Nome e CPF
    fields = set(data.keys())
    validate_fields = set(Empresa.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
    flag_ir_error = False
    for key, value in data.items():
        if value.strip() in ['', None]:
            flag_ir_error = True
    if not validate_fields or flag_ir_error:
        raise Exception('Nome e CNPJ são obrigatórios')

    # 2 - Se exitir qualquer outro parametro que contains os fields do Endereço,
    # precisamos garantir que todos os fields de Endereço existam.from
    fields = data.keys()
    flag_is_exists_fiels = any(i in Endereco.VALIDATE_FIELDS_REQUIREMENTS for i in fields)
    if flag_is_exists_fiels:
        fields = set(data.keys())
        fields.remove('nome')
        fields.remove('cnpj')
        validate_fields = set(Endereco.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
        flag_ir_error = False
        for key, value in data.items():
            if value in ['', None]:
                flag_ir_error = True
        if not validate_fields or flag_ir_error:
            raise Exception('Todos os campos do endereço são obrigatórios')
