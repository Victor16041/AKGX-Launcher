# AKGX Launcher

AKGX Launcher é um aplicativo desenvolvido em Python por mim e meus amigos para o nosso TCC. O objetivo principal do projeto é criar uma ferramenta para pesquisa e gerenciamento de downloads utilizando o protocolo BitTorrent.

A ideia do projeto surgiu da necessidade de centralizar a organização de bibliotecas de jogos e facilitar o gerenciamento dos downloads em uma única aplicação, evitando a necessidade de utilizar diversas ferramentas separadas.

O projeto possui um backend desenvolvido em FastAPI, responsável pelo gerenciamento dos downloads e comunicação com APIs externas, e uma interface gráfica desenvolvida em PyQt5 para pesquisa, visualização de informações e acompanhamento dos downloads.

---

# Público-alvo

Entusiastas de jogos e desenvolvedores interessados em criar ferramentas para gerenciamento de bibliotecas, organização de informações e gerenciamento de downloads utilizando o protocolo BitTorrent.

---

# Funcionalidades

- Pesquisa de jogos por nome.
- Busca automática de capas utilizando a SteamGridDB.
- Início de downloads por links Magnet.
- Acompanhamento do progresso, velocidade e quantidade de peers em tempo real.
- Organização dos downloads em uma interface gráfica simples.
- Gerenciamento de downloads ativos.

---

# Tecnologias utilizadas

## Linguagem

- Python

## Frameworks e bibliotecas

- FastAPI
- PyQt5
- libtorrent
- Requests

## APIs utilizadas

- SteamGridDB API

## Armazenamento de dados

O projeto utiliza arquivos JSON para armazenar informações dos catálogos de downloads.

---

# Arquitetura do sistema

O sistema é dividido em duas partes principais:

## Frontend

Desenvolvido utilizando PyQt5.

Responsável por:

- Interface gráfica;
- Pesquisa de jogos;
- Exibição de capas;
- Visualização do progresso dos downloads.

## Backend

Desenvolvido utilizando FastAPI.

Responsável por:

- Gerenciamento dos downloads;
- Comunicação com o libtorrent;
- Busca de informações dos jogos;
- Retorno dos dados para o frontend.

Fluxo básico:

Usuário  
↓  
Interface PyQt5  
↓  
Requisições HTTP  
↓  
Backend FastAPI  
↓  
libtorrent  
↓  
Gerenciamento dos downloads

---

# Estrutura do projeto
