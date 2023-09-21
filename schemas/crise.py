from pydantic import BaseModel, validator, Field
from typing import Optional, List
from model.crise import Crise
from datetime import date
import re


class CriseSchema(BaseModel):
    """ Define como uma nova crise deve ser inserida
    """
    data_crise: str = "04/07/2023"
    nome: str = "Jose Bezerra da Silva - Processo trabalhista"
    prazo: int = 15
    detalhes: str = "O colocaborador Jose , solicitou indenização trabalista , pedindo correção das horas extras trabalhadas no período de 01/01/2023 até 30/05/2023. Alegando ter trabalhado e não ter recebido"
    
    @validator('data_crise')
    def valida_data_crise(cls, v):
        if re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", v):
            return v
        raise ValueError('A data tem que estar no formato dd/mm/aaaa')
    
class UpdateCriseSchema(BaseModel):
    """ Define como uma crise pode ser atualizada.
    """
    id: int = "10"
    data_crise: str = "04/07/2023"
    nome: str = "Colaborador Jose Bezerra da Silva - Processo trabalhista"
    prazo: int = 15
    detalhes: str = "O colocaborador Jose , solicitou indenização trabalista , pedindo correção das horas extras trabalhadas no período de 01/01/2023 até 30/05/2023. Alegando ter trabalhado e não ter recebido"
    

class CriseBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na id da crise.
    """
    #nome: str = "nome"
    id: int = 1
    # id: int = "10"
    #data_crise: str = "04/07/2023"
    #nome: str = "Colaborador Jose Bezerra da Silva - Processo trabalhista"
    #prazo: int = 15
    #detalhes: str = "O colocaborador Jose , solicitou indenização trabalista"

class CriseDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
   #nome: str = "nome" 
    id: int = 1



class ListagemCriseSchema(BaseModel):
    """ Define como uma listagem de crises será retornada.
    """
    crises:List[CriseSchema]


def apresenta_crises(crises: List[Crise]):
    """ Retorna uma representação da Crise seguindo o schema definido em
        CriseViewSchema.
    """
    result = []
    for crise in crises:
        result.append({
            "id": crise.id,
            "data_crise": crise.data_crise,
            "nome": crise.nome,
            "prazo": crise.prazo,
            "detalhes": crise.detalhes,        
        })

    return {"Crises": result}


class CriseViewSchema(BaseModel):
    """ Define como uma crise será retornado: crise .
    """
    id: int = 1
    data_crise: date = '04/07/2023'
    nome: str = "Colaborador Jose Bezerra da Silva - Processo trabalhista"
    prazo: int = 30
    detalhes: str = "O colocaborador Jose , solicitou indenização trabalista , pedindo correção das horas extras trabalhadas no período de 01/01/2023 até 30/05/2023. Alegando ter trabalhado e não ter recebido"
       



def apresenta_crise(crise: Crise):
    """ Retorna uma representação da crise seguindo o schema definido em
        CriseViewSchema.
    """
    return {
        "id": crise.id,
        "data_crise": crise.data_crise,
        "nome": crise.nome,
        "prazo": crise.prazo,
        "detalhes": crise.detalhes,
    }

