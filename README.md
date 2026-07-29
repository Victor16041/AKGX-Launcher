# AKGX Launcher

AKGX Launcher é um aplicativo desenvolvido em Python por mim e meus amigos para o nosso TCC. O objetivo do projeto é criar uma ferramenta para pesquisa e gerenciamento de downloads utilizando o protocolo BitTorrent.

A ideia do projeto é facilitar a organização de bibliotecas de jogos, juntando em um único aplicativo a pesquisa de jogos, visualização de informações e gerenciamento dos downloads.

O projeto possui um backend desenvolvido em FastAPI, responsável pelo controle dos downloads e comunicação com serviços externos, e uma interface gráfica feita em PyQt5 para interação com o usuário.

---

# Público-alvo

Entusiastas de jogos e desenvolvedores interessados em ferramentas de organização de bibliotecas, gerenciamento de informações e downloads utilizando o protocolo BitTorrent.

---

# Funcionalidades

- Pesquisa de jogos por nome.
- Busca automática de capas utilizando a SteamGridDB.
- Início de downloads por links Magnet.
- Acompanhamento do progresso, velocidade e quantidade de peers em tempo real.
- Organização dos downloads em uma interface simples.

---

# Tecnologias utilizadas

- Python
- FastAPI
- PyQt5
- libtorrent
- Requests
- SteamGridDB API

---

# Arquitetura do sistema

O projeto é dividido em duas partes:

## Backend

O backend foi desenvolvido utilizando FastAPI e é responsável por:

- Gerenciar os downloads.
- Controlar o libtorrent.
- Buscar informações dos jogos.
- Enviar informações para a interface.

## Interface

A interface foi desenvolvida utilizando PyQt5 e é responsável por:

- Pesquisa de jogos.
- Exibição das capas.
- Mostrar informações dos downloads.
- Acompanhar o progresso.

Fluxo do sistema:

```
Usuário
   |
   v
Interface PyQt5
   |
   v
Backend FastAPI
   |
   v
libtorrent
   |
   v
Downloads
```

---

# Como usar

## 1) Instale as dependências:

```bash
pip install -r requirements.txt
```

## 2) Crie um arquivo `fonte1.json` seguindo este modelo:

```json
{
    "name": "Nome da Fonte",
    "downloads": [
        {
            "title": "Nome do Jogo",
            "uris": [
                "magnet:?xt=..."
            ],
            "uploadDate": "2026-06-17T01:10:56.000",
            "fileSize": "47.8 GB"
        }
    ]
}
```

Adicione quantos objetos forem necessários dentro de `downloads`, um para cada jogo do catálogo.

## 3) Adicione sua chave da SteamGridDB no arquivo `backend.py`:

```python
API_KEY = "SUA_API_KEY"
```

## 4) Execute o backend:

```bash
uvicorn backend:app --reload
```

## 5) Execute a interface:

```bash
python main.py
```

---

# Backend API

Principais rotas:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/buscar/{nome}` | Pesquisa jogos pelo nome |
| GET | `/download/{id}` | Inicia um download |
| GET | `/status/{id}` | Mostra o status do download |
| GET | `/downloads` | Lista downloads ativos |
| GET | `/cancelar/{id}` | Cancela um download |

---

# Telas do sistema

## Tela de Pesquisa

Responsável pela busca dos jogos disponíveis no catálogo.

Possui:

- Campo de pesquisa.
- Exibição das capas.
- Botão para iniciar download.

## Tela de Downloads

Responsável por mostrar os downloads em andamento.

Possui:

- Barra de progresso.
- Velocidade de download.
- Quantidade de peers.
- Status do download.
- Botão para abrir a pasta.

---

# Banco de dados

O projeto não utiliza banco de dados.

As informações dos jogos são armazenadas utilizando arquivos JSON, que funcionam como uma fonte de dados para o sistema.

---

# Aviso

Este repositório contém apenas o código-fonte do projeto. Nenhum arquivo Magnet, catálogo de downloads ou conteúdo protegido por direitos autorais é distribuído junto com a aplicação.
