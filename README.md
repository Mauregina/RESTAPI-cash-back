# Carteira Digital

Problema
--------

Uma grande rede varegista do ramo alimentício, irá utilizar a carteira digital da MaisTODOS para dar cashback para os seus clientes e gerar vendas campanhas, etc.

Então basicamente vamos precisar de uma API para fazer todo o gerenciamento desses valores e repassar para uma outra API de cashback para dar ao cliente o valor do benefício de fato.

Na API, ficaria toda a lógica e controle da aplicação do cashback.
Fique livre para definir a regra de aplicação
- Ex: 10% do valor total
- Ex2: Fazer por type de produto, tipo A possui 5% e tipo B possui 15%

Sendo responsável pelas seguintes ações:
- Recebe os dados via API
- Faz o processamento dos dados
- Faz uma nova requisição para uma API externa de cashback da MaisTODOS


Fluxograma
----------

1 - ERP do varegista faz a requisição nesta API a ser construída:

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
          "qty": 9,
       }
    ],
}
```

Onde:
- customer -> document: é o cpf do cliente
- products -> type: é a classificação do produto, você irá definir os valores mas podemos usar (A, B, C)
- products -> value: é o valor unitário do produto
- products -> qty: é a quantidade de cada produto

2 - A API recebe e faz a validação os dados

Exemplos de validação:
- cpf inválido
- soma errada dos valores
- type de produto fora do formato
- data inválida

3 - A API deve salvar todos os dados recebidos, para termos como conciliar posteriormente com o cliente. Bem como o retorno da API de cashback, para gestão de reenvios, etc.

4 - A API será responsável por todo o cálculo de cashback (Fique livre para definir as regras)

5 - Com os valores já corretos, vamos repassar o valor do cashback para uma API da MaisTODOS criar o cashback de fato

Seguem exemplos da requisição e resposta da API externa da MaisTODOS de cashback:

```
URL: https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback
Método: POST
Data: document -> Cpf do cliente
      cashback -> valor calculado
```

Exemplo com o curl

```curl
curl --request POST \
  --url https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback \
  --header 'Content-Type: application/json' \
  --data '{
	"document": "33535353535",
	"cashback": "10"
}'
```

Retorno da api:

```json
{
  "createdAt": "2021-07-26T22:50:55.740Z",
  "message": "Cashback criado com sucesso!",
  "id": "NaN",
  "document": "33535353535",
  "cashback": "10"
}
```

## Ferramentas utilizadas na solução

* Visual Studio SCode
* Python 3.9.10
* Flask
* SQLite
* Postman
```sh
pip install -r requirements.txt 
```
