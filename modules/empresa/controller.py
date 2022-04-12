from flask import Blueprint, request, jsonify, make_response, Response
from modules.empresa.dao import EmpresaDao
from modules.empresa.modelo import Empresa
from utils.database import ConnectSingletonDB
import traceback

app_empresa = Blueprint('app_empresa', __name__)
app_name = "empresa"
dao = EmpresaDao(database=ConnectSingletonDB())


@app_empresa.route('/{}/'.format(app_name),
                   methods=['GET'])
def get_empresas():
    empresas = dao.get_all()
    return make_response(jsonify(empresas), 200)


@app_empresa.route('/{}/add/'.format(app_name),
                   methods=['POST'])
def add_empresa():
    data = request.form.to_dict(flat=True)
    empresa = None
    try:
        empresa = Empresa(**data)
        empresa = dao.save(empresa)
    except Exception as e:
        print(traceback.format_exc())
        return make_response(
            {
                'error': True,
                'message': 'Nome e CNPJ são obrigatórios'
            }, 400)
    return make_response({'id': empresa.id}, 201)
