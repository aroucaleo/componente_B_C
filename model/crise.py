from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Union

from  model import Base


class Crise(Base):
    __tablename__ = 'crise'

    id = Column("pk_crise", Integer, primary_key=True)
    data_crise = Column(String(20))
    nome = Column(String(200))
    prazo = Column(Integer)
    detalhes = Column(String(8000))
    data_insercao = Column(DateTime, default=datetime.now())
    

    def __init__(self, data_crise:date, nome:str, prazo:int, detalhes:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma crise

        Arguments:
            nome: titulo da crise.
            detalhes: descrição da crise 
            prazo: quantidade de dias para solução da crise
            data_crise: data que ocorreu a crise 
            data_insercao: data de quando a crise foi inserido à base
        """
        
        self.data_crise = data_crise
        self.nome = nome
        self.prazo = prazo
        self.detalhes = detalhes        
        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao



