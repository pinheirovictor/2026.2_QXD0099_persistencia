# QXD0099 — FastAPI + JSON + YAML + Logging

Projeto didático com uma única entidade: **Livro**.

## Conteúdos trabalhados

- FastAPI
- JSON
- serialização e desserialização
- Pydantic
- `model_dump(mode="json")`
- JSON Schema
- persistência em arquivo JSON
- YAML
- logging
- CRUD

## Estrutura

```text
fastapi_livros_json_yaml_qxd0099/
├── main.py
├── logging.yaml
├── requirements.txt
├── core/
│   └── logging_config.py
├── models/
│   └── livro.py
├── routes/
│   └── livros.py
├── services/
│   └── json_repository.py
└── data/
    └── livros.json
```

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Execução

Na raiz do projeto:

```bash
uvicorn main:app --reload
```

## Swagger

Acesse:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

```text
POST   /livros
GET    /livros
GET    /livros/{id}
PUT    /livros/{id}
DELETE /livros/{id}
```

## Exemplo de POST /livros

```json
{
  "id": 2,
  "titulo": "Sistemas de Banco de Dados",
  "autor": "Elmasri e Navathe",
  "ano": 2011,
  "categorias": [
    "Banco de Dados",
    "Computação"
  ],
  "disponivel": true
}
```

## Persistência

Os dados são gravados em:

```text
data/livros.json
```

## Logging

A configuração está em:

```text
logging.yaml
```

Os eventos são persistidos em:

```text
app.log
```
