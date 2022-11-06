# SQL-Project

Neste projeto da disciplina de Megadados, foi desenvolvido um **microsserviço de controle de estoque** usando o framework **FastAPI**.

## Membros da dupla

- Luca Coutinho Melão
- Matheus Kwon

## Requisitos funcionais

O usuário pode criar produto, consultar inventário de produtos, alterar detalhes do produto, alterar quantidade de produto, remover produto do inventário.

- Criar Produto **[POST]**

- Consultar inventário de produtos completo **[GET]**

- Consultar produto no inventário **[GET]**

- Alterar detalhes de produtos **[PUT]**

- Alterar a quantidade de produtos **[PATCH]**

- Remover produtos do inventário **[DELETE]**

## Documentação visual

Acesse para testar as requisições e as funcionalidades da API e para compreender sua documentação.

- Swagger UI (URL/docs):

```shell
http://127.0.0.1:8000/docs
```

- ReDoc (URL/redoc):

```shell
http://127.0.0.1:8000/redoc
```

## Comandos

Infraestrutura:

```shell
pip3 install -r requirements.txt
export DATABASE_URL="mysql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
```

Variáveis que devem ser substituídas:

- {USER} = Usuário do servidor
- {PASSWORD} = Senha do usuário
- {SERVER} = Endereço IP do servidor
- {DATABASE} = Nome da base de dados

Ao abrir o MySQL Workbench você deve ver {DATABASE} em schemas.

Para confirmar, rode o comando abaixo:

```shell
echo $DATABASE_URL
```

App:
```shell
uvicorn main:app --reload
```