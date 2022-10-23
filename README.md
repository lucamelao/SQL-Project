# SQL-Project

---

Neste projeto da disciplina de Megadados, foi desenvolvido um **microsserviço de controle de estoque** usando o framework **FastAPI**.

## Membros da dupla

---

- Luca Coutinho Melão
- Matheus Kwon

## Requisitos funcionais

---
Usuário pode criar produto, consultar inventário de produtos, alterar detalhes do produto, alterar quantidade de produto, remover produto do inventário.

- Criar Produto [POST]

- Consultar inventário de produtos [GET]

- Alterar detalhes de produtos [PUT]

- Alterar a quantidade de produtos [PATCH]

- Remover produtos do inventário [DELETE]

## Interfaces visuais

---

- Swagger UI (URL/docs)
- ReDoc (URL/redoc)

---

Ativação do environment:

```shell
source env/bin/activate
```

Run app:

```shell
uvicorn main:app --reload
```