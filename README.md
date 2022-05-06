## Carteira Digital
1. API recebe, valida e salva dados da compra, bem como calcula o valor do cash back.

```
POST /api/cashback 
```

```shell
{
    "sold_at": "2026-01-02 00:00:00",
    "customer": {
       "document": "00000000000",
       "name": "JOSE DA SILVA",
    },
    "total": "100.00",
    "products": [
       {
          "type": "A",
          "value": "10.00",
          "qty": 1,
       },
       {
          "type": "B",
          "value": "10.00",
          "qty": 9
       }
    ]
}
```

Onde:
- customer -> document: é o cpf do cliente
- products -> type: é a classificação do produto, você irá definir os valores mas podemos usar (A, B, C)
- products -> value: é o valor unitário do produto
- products -> qty: é a quantidade de cada produto

5 - Repassa o valor do cashback para uma API da MaisTODOS.

```
URL: https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback
Método: POST
Data: document -> Cpf do cliente
      cashback -> valor calculado
```

Retorno da API:

```json
{
  "createdAt": "2021-07-26T22:50:55.740Z",
  "message": "Cashback criado com sucesso!",
  "id": "NaN",
  "document": "33535353535",
  "cashback": "10"
}
```

## Modelo Lógico
<p align="center"> <img src=/logic_model/logic_model.png alt="model" class="center"></p>

## Ferramentas utilizadas na solução
* Visual Studio SCode
* Python 3.9.10
* Flask
* SQLAlchemy
* SQLite
* Postman
```sh
pip install -r requirements.txt 
```

## 
