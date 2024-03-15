# prod-camp-onmaps

# API 

Projeto que sobe um Container e, neste, uma API RESTful com o Swagger

## Getting Started

Para executar a aplicação, basta compilar o Docker e executar o mesmo com os seguintes comandos

```
docker-compose build
docker-compose up
```

Há ainda um arquivo chamado 'api_consulta_simples.py', onde a consulta é mais simples e não precisa copilar o Docker. Apenas executar o script, e estará disponível para consumo. No mesmo arquivo há comentários para o script.

## Estrutura do Projeto

A estrutura do projeto segue um padrão organizacional para facilitar a manutenção e escalabilidade:

- service: Contém o código principal da aplicação.
- config: Arquivo de configurações gerais.
- constants: Armazena códigos de retorno HTTP e textos de respostas principais.
- controller: Declaração dos endpoints servidos pela aplicação.
- responses: Código para a construção da resposta.
- service: Código do serviço oferecido.
- util: Códigos diversos.
- init.py: Configurações e início do aplicativo.
- main.py: Início do aplicativo.
- app.py: Configuração da API e inicialização dos endpoints.
- logging.conf: Configuração do logger.
- restplus.py: Configuração da API RESTful.
- settings.py: Variáveis e configurações.
- docker-compose.yml: Configuração do container Docker.
- Dockerfile.dev: Configuração do container Docker.
- README.md: Documentação do projeto.
- setup.py: Pré-requisitos da aplicação.

## Funcionamento da Aplicação

1. Construção e Inicialização do Container:

    - Utiliza-se o comando docker-compose build para construir o container com as especificações corretas.
    - O comando docker-compose up sobe o serviço.

2. Inicialização do Swagger:

- O arquivo service/app.py inicializa os endpoints da aplicação, incluindo:
    - /docs com a página principal.
    - service/controller/start_controller: /.
    - service/controller/main_controller: /main.

3. Processamento de Requisições:

- Ao receber uma requisição em /main:
    - O arquivo service/controller/main_controller.py carrega o endpoint e realiza testes de conformidade.
    - O objeto service.service.main_service carrega o modelo.
    - O parâmetro passado é processado pelo modelo.
    - A resposta é enviada.

## Exemplos de Funcionamento da API

<b> Exemplo 1:</b>

http://localhost:5000/predict?lat=-22.8232257917&lng=-47.0758807513

<b>Resposta:</b>

{"latitude":-22.8232257917,"longitude":-47.0758807513,"n_grandes_redes":0 "n_pequeno_varejista":1,"predicao":2303.7645920145533}


<b>Exemplo 2:</b>

http://localhost:5000/predict?lat=-22.8053524424&lng=-47.0064121403

<b>Resposta:</b>

{"latitude":-22.8053524424,"longitude":-47.0064121403,"n_grandes_redes":0,"n_pequeno_varejista":0,"predicao":2462.717120543708}


<b>Exemplo 3:</b> 

http://localhost:5000/predict?lat=-22.982356215&lng=-46.9112167395

<b>Resposta:</b>

{"error":"The provided coordinates are not within the municipality of Campinas"}



## Autores

* **Danilo Medeiros** - *Trabalho inicial*

## Exemplo de template copiado de: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2

