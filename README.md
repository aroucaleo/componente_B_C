# API REST - GESTOR DE CRISES

Este projeto tem como objetivo desenvolvimento de um getor de crises empresarial.
O projeto foi desenvolvido da seguinte forma:

Componente A - Front End ( Html, css e javacript)
-->Front end exibe informações que são inseridas pela conexão via api externa automatica e também pode ter a inserção de dados manual pelo proprio front end

Componente B - Arquivo app.py com uma rota em especial , chamada CRISESAPI , que é o componente b que conecta com a api externa e consome as informações e são armazenadas no banco de dados da aplicação
--> informaçoes para acesso a api externa estão dentro da rota  CRISESAPI  

Componente C - Back End  ( API REST )
--> app.py - rotas GET,DELETE,POST E PUT, implementadas de acordo com a necessidade da aplicação .


 **PUC-RIO - Desenvolvimento Full Stack - por: Leonardo Arouca** 

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Back-end Avançado Sprint II** 


O objetivo aqui é apresetar uma API seguindo o estilo REST.

As principais tecnologias que serão utilizadas aqui é o:
 - [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - [SQLAlchemy](https://www.sqlalchemy.org/)
 - [OpenAPI3](https://swagger.io/specification/)
 - [SQLite](https://www.sqlite.org/index.html)

---
### Para Instalação

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando o servidor...

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---
### Acesso no browser

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.


---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t backcrises .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -it -p 5000:5000 backcrises
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### Alguns comandos úteis do Docker

**Para verificar se a imagem foi criada** você pode executar o seguinte comando:

```
$ docker images
```

 Caso queira **remover uma imagem**, basta executar o comando:
```
$ docker rmi <IMAGE ID>
```
Subistituindo o `IMAGE ID` pelo código da imagem

**Para verificar se o container está em exceução** você pode executar o seguinte comando:

```
$ docker container ls --all
```

 Caso queira **parar um conatiner**, basta executar o comando:
```
$ docker stop <CONTAINER ID>
```
Subistituindo o `CONTAINER ID` pelo ID do conatiner


 Caso queira **destruir um conatiner**, basta executar o comando:
```
$ docker rm <CONTAINER ID>
```
Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).