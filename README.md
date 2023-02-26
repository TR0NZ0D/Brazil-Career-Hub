# Job Finder - TCC
Reposiório destinado ao desenvolvimento do TCC do curso de Ciências da Computação 2023 - UNIP

## Pipelines / Workflows

|  Branch  |  Status  |
| :------: | :----: |
| Development | [![Django CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml/badge.svg?branch=development)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml) |
| Development | [![Pylint Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml/badge.svg?branch=development)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml) |
| -------------------- | --------------------- | ------------------------------------ |
| Production | [![Django CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml/badge.svg?branch=production)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml) |
| Production | [![Pylint Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml/badge.svg?branch=production)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml) |



## Integrantes

|  Nome  |  RA  |
| ------ | ---- |
| Carlos Eduardo dos Santos Ferreira | N6401C7 |
| Gabriel Menezes de Antonio | F13GJI6 |
| Gustavo Henrique Dos Santos Faria | F22IFG2 |
| Mayara Marques Pereira de Souza | N542DD1 |

## Arquitetura

- **Front-end:** React
- **Back-end:** Django
- **Database:** MySQL
- **Idiomas:** Português & Inglês
- **Ui Spec:** Figma
- **Hosting Server:** AWS
- **Hosting OS:** Linux - Ubuntu

## Dependências

**Base**
| Pacote | Versão |
| ------ | ------ |
| Python |  3.11  |
|  Node  | 19.2.0 |
|  npm   | 9.2.0  |

**Bibliotecas**
- Vide arquivo `requirements.txt`

## Instalação

1. Certifique-se ter instalado as dependências base

2. Navegue até o diretório `[...]/TCC-CC`

3. Crie um ambiente virtual <br>
    **Ubuntu:** python3.11 -m venv venv <br>
    **Windows:** python3 -m venv venv

4. Ative o ambiente virtual <br>
    **Ubuntu:** `source venv/bin/activate` <br>
    **Windows:** `/venv/scripts/activate.bat`

5. Atualize as versões do `pip`, `setuptools` e `wheel`
    > `pip install --upgrade pip setuptools wheel`

6. Instale os requisitos a partir do arquivo
    > `pip install --upgrade -r requirements.txt`

7. Instale os pacotes de front-end NPM
    > `npm install`

## Executando o Projeto

O projeto consiste em dois ambientes, front-end e back-end. O back-end é responsável pela API e entrega de informações e dados do banco para o front-end, o qual, por sua vez, é responsável pela exibição e atualização dos dados do back-end.

Ambos os ambientes devem estar rodando para que o projeto possa ser executado corretamente.

**Executando ambiente back-end:** 

Para executar o ambiente de back-end é necessário estar em um ambiente virtual (venv) com todos os requisitos instalados.

1. Antes de iniciar, cheque se está com a última atualização do banco, lembre-se de nunca acessar o banco de produção.
    > `python manage.py makemigrations && python manage.py migrate`

2. Em seguida, cheque o projeto em busca de erros.
    > `python manage.py check`

3. Caso esteja tudo certo, execute o projeto
    > `python manage.py runserver 0.0.0.0:8000 --insecure`

4. Para acessar a documentação da API, acesse o link
    > `http://0.0.0.0:8000/api/docs`

    Caso tenha alterado o IP no comando do passo anterior, acesse o link que é exibido no terminal e acrescente `/api/docs` no final da URL.

**Executando ambiente front-end:**

Para executar o ambiente de front-end, é necessário ter todos os requisitos instalados na máquina

> `npm start`

## Realizando chamadas para API e endpoints

Para realizar uma chamada para API, realize um request (GET / POST / PUT / DELETE) para a URL do site acrescentada com `/api/<comando>`

E.g.: Caso a URL do site seja `https://JobFinder.com` e gostaríamos de requisitar o status da API, o endpoint da chamada seria `https://JobFinder.com/api/status`.

## Links

- [Figma Project](https://www.figma.com/files/project/76812132/Job-Finder---TCC?fuid=1085988712828291035)
- [Site em produção [ip]](https://54.175.223.130/)

## Conexão ao servidor

- **DNS:** ec2-54-175-223-130.compute-1.amazonaws.com
- **SSH PEM Key:** Job_Finder_TCC_CC.pem
- **Username:** ubuntu

## Contas de usuário

| Username | Password | Authorization level |
| -------- | -------- | ------------------- |
| ApiAdmin | XJpU7iUw8BuZ5tT | Staff (Read only) |

## Postman

Para utilizar o postman, importe a coleção `TCC-CC/tests/postman/JobFinderAPI.postman_collection.json` para o postman.

Para importar, no postman, no canto superior esquerdo da tela, clique no botão "Import" ao lado do nome do workspace.

Ao clicar no botão irá abrir um prompt para importar um arquivo, importe o arquivo `JobFinderAPI.postman_collection.json` presente no repositório do projeto.

Ao importar, você verá os endpoint divididos em pastas, por padrão, estamos utilizando variáveis da coleção para tratar autorizações, o usuário padrão é o `ApiAdmin`. Caso prefire, crie um ambiente virtual e insira as credenciais do seu usuário.

## Licença

**GNU GPL v3**

- **Permissões:** Uso comercial, distribuição, modificação, uso de parente e uso privado do software.

- **Condições:** Divulgar o código-fonte, exibir os avisos de licença e direitos autorais, declarar todas as alterações e nomear as bibliotecas sob a mesma licença.

- **Limitações:** Incluir informações de responsabilidade e garantia no trabalho.
