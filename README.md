# Brazil Career Hub

Reposiório destinado ao desenvolvimento do TCC do curso de Ciências da Computação 2023 - UNIP

## Pipelines / Workflows

|  Development  |  Production  |
| :------: | :----: |
| [![Django CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml/badge.svg?branch=development)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml) | [![Django CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml/badge.svg?branch=production)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/django.yml) |
| [![Pylint Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml/badge.svg?branch=development)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml) | [![Pylint Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml/badge.svg?branch=production)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/pylint.yml) |
| [![npm CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/node.js.yml/badge.svg?branch=development)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/node.js.yml) | [![npm CI Status](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/node.js.yml/badge.svg?branch=production)](https://github.com/TR0NZ0D/TCC-CC/actions/workflows/node.js.yml) |

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

### Base

| Pacote | Versão |
| ------ | ------ |
| Python |  3.11  |
|  Node  | 19.2.0 |
|  npm   | 9.2.0  |

### Bibliotecas

- Vide arquivo `requirements.txt` de cada ambiente.

## Instalação

A instalação de cada ambiente pode ter sua especificidade.

### Instalação back-end

Para instalar o ambiente back end, simplesmente execute o arquivo `source\back-end\run-back-end.bat`.

Este arquivo criará todos os itens necessários.

Caso esteja executando no powershell, antes de rodar o arquivo batch, execute o seguinte comando em um terminal com permissões administrativas:

``` shell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Executando o Projeto

O projeto consiste em dois ambientes, front-end e back-end. O back-end é responsável pela API e entrega de informações e dados do banco para o front-end, o qual, por sua vez, é responsável pela exibição e atualização dos dados do back-end.

Ambos os ambientes devem estar rodando para que o projeto possa ser executado corretamente.

### Executando ambiente back-end

Para executar o ambiente back end, simplesmente execute o arquivo `source\back-end\run-back-end.bat`.

Este arquivo criará todos os itens necessários.

Caso esteja executando no powershell, antes de rodar o arquivo batch, execute o seguinte comando em um terminal com permissões administrativas:

``` shell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Executando ambiente front-end:

Para executar o ambiente de front-end, é necessário ter todos os requisitos instalados na máquina

``` shell
npm start
```

## Realizando chamadas para API e endpoints

Para realizar uma chamada para API, realize um request (GET / POST / PUT / DELETE) para a URL do site acrescentada com `/api/<comando>`

E.g.: Caso a URL do site seja `https://BrazilCareerHub.com` e gostaríamos de requisitar o status da API, o endpoint da chamada seria `https://BrazilCareerHub.com/api/status`.

## Links

- [Figma Project](https://www.figma.com/files/project/76812132/Brazil-Career-Hub---TCC?fuid=1085988712828291035)

## Contas de usuário

| Username | Password | Authorization level |
| -------- | -------- | ------------------- |
| ApiAdmin | XJpU7iUw8BuZ5tT | Staff (Read only) |

## Postman

[Importe os arquivos](./Postman/)

## Licença

### GNU GPL v3

- **Permissões:** Uso comercial, distribuição, modificação, uso de parente e uso privado do software.

- **Condições:** Divulgar o código-fonte, exibir os avisos de licença e direitos autorais, declarar todas as alterações e nomear as bibliotecas sob a mesma licença.

- **Limitações:** Incluir informações de responsabilidade e garantia no trabalho.
