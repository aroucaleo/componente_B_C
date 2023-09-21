import requests
import pprint
import json
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Crise
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="Gestor de crises empresarial", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
crise_tag = Tag(name="Gestor de Crises", description="Adição, atualização , visualização e remoção de crises à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/crise', tags=[crise_tag],
          responses={"200": CriseViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_crise(form: CriseSchema):
    """Adiciona uma nova Crise à base de dados

    Retorna uma representação das crises.
    """
    crise = Crise(
        data_crise=form.data_crise,
        nome=form.nome,
        prazo=form.prazo,
        detalhes=form.detalhes
        )
    logger.debug(f"Adicionando uma crise de nome: '{crise.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(crise)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado uma crise de nome: '{crise.nome}'")
        return apresenta_crise(crise), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Uma crise do mesmo nome já foi salva na base :/"
        logger.warning(f"Erro ao adicionar uma crise '{crise.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova crise :/"
        logger.warning(f"Erro ao adicionar uma crise '{crise.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/crises', tags=[crise_tag],
         responses={"200": ListagemCriseSchema, "404": ErrorSchema})
def get_crise():
    """Faz a busca por todas as Crises cadastradas

    Retorna uma representação da listagem de crises.
    """
    logger.debug(f"Coletando crises da base de dados ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    crises = session.query(Crise).order_by(Crise.prazo.asc()).all()

    if not crises:
        # se não há crises cadastradas
        return {"crises": []}, 200
    else:
        logger.debug(f"%d crises econtrados" % len(crises))
        # retorna a representação de uma crise
        print(crises)
        return apresenta_crises(crises), 200


@app.delete('/crise', tags=[crise_tag],
            responses={"200": CriseDelSchema, "404": ErrorSchema})
def del_crise(query: CriseBuscaSchema):
    """Deleta uma  Crise a partir da id da crise informada

    Retorna uma mensagem de confirmação da remoção.
    """
    crise_id = query.id
    print(crise_id)
    logger.debug(f"Deletando dados sobre crise #{crise_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Crise).filter(Crise.id == crise_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado crise #{crise_id}")
        return {"mesage": "Crise removida", "id": crise_id}
    else:
        # se a crise não foi encontrado
        error_msg = "Crise não encontrado na base :/"
        logger.warning(f"Erro ao deletar crise #'{crise_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    
@app.put('/updateCrise', tags=[crise_tag],
          responses={"200": CriseViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_crise(form: UpdateCriseSchema):
    """Edita uma crise já salvo na base de dados

    Retorna uma representação das crises.
    """
    id_crise = form.id
    session = Session()

    try:
        query = session.query(Crise).filter(Crise.id == id_crise)
        print(query)
        db_crise = query.first()
        if not db_crise:
            # crise não foi encontrada
            error_msg = "Crise não encontrado na base :/"
            logger.warning(f"Erro ao buscar crise '{id_crise}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            if form.nome:
                db_crise.nome = form.nome
            if form.data_crise:  
                db_crise.data_crise = form.data_crise
            if form.detalhes:
                db_crise.detalhes=form.detalhes
            if form.prazo:
                db_crise.prazo=form.prazo
            
            session.add(db_crise)
            session.commit()
            logger.debug(f"Editado usuario de id: '{db_crise.id}'")
            return apresenta_crise(db_crise), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar usuario '{db_crise.id}', {error_msg}")
        return {"mesage": error_msg}, 400

  
@app.get('/crisesapi', tags=[crise_tag],
         responses={"200": ListagemCriseSchema, "404": ErrorSchema})
def get_crisesapi():     
    """Faz a busca pelas crises da api externa e adiona no banco de dados

    Retorna as crises da api externa
    """

    headers = {
    "accept": "application/json",
    "cobli-api-key": "WKNPnuj.67557cb1-0ed7-4b39-8999-8bcc798fc69c"
    }

    # fazendo uma requisição get
    request = requests.get("https://api.cobli.co/public/v1/risk-events/?start_date=2023-05-01&end_date=2023-10-01&timezone=America%2FSao_Paulo&limit=1000&page=1", headers=headers)
    dados = request.json()
    pprint.pprint(dados)

    #tabela = pd.DataFrame(dados['data'])
    #print(tabela)

    if __name__ == '__main__':
        get_crisesapi()
    

    if request.status_code == 200:
        indice = 0
        nome_motorista = dados['data'][indice]['driver']['name']
        veiculo = dados['data'][indice]['vehicle']['license_plate']
        evento = dados['data'][indice]['event_type']
        info_evento = evento + " for the vehicle license plate " + veiculo
        data_api= dados['data'][indice]['event_time']
        data_eua= data_api[0:10]
        data_ev = data_eua.split('-', 2)
        data_evento = data_ev[2] + '/' + data_ev[1] + '/' + data_ev[0]
        ev_prazo = 1

        crise = Crise(
                    data_crise=data_evento,
                    nome=nome_motorista,
                    prazo=ev_prazo,
                    detalhes=info_evento
                    )
        #  criando conexão com a base
        session = Session()
        # adicionando CRISE
        session.add(crise)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Informações da API externa adicionada na base de dados: '{crise.nome}'")

        print('==================================================================')
        print('Dados da API externa salvos no banco de dados')
        print('==================================================================')
        print('Data - ', data_api)
        print('Data - ', data_evento)
        print('Nome - ', nome_motorista)
        print('Prazo - ', ev_prazo, 'dia(s)')
        print('Detalhes - ', info_evento)
        print('==================================================================')
    else:
        print('Não foi possível acessar as informações.')
    logger.debug(f"Coletando usuarios ")
    # criando conexão com a base
    session = Session()
    crises = session.query(Crise).order_by(Crise.nome.asc()).all()
    
    if not crise:
        # se não há usuarios cadastrados
        return {"Crises": []}, 200
    else:
        logger.debug(f"%d crises econtrados" % len(crises))
        # retorna a representação do fornecedor
        print(crises)
        return apresenta_crises(crises), 200