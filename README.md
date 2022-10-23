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
pip install -r requirements.txt
```

App:

```shell
uvicorn main:app --reload
```