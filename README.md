AKGX Launcher é um aplicativo desenvolvido em Python por mim e meus amigos para o nosso TCC, o objetivo principal dele é pesquisar e gerenciar downloads através do protocolo BitTorrent. O projeto possui um backend em FastAPI responsável pelo gerenciamento dos downloads e uma interface gráfica em PyQt5 para pesquisa, acompanhamento do progresso e organização dos downloads.

Funcionalidades:
- Pesquisa de jogos por nome.
- Busca automática de capas utilizando a SteamGridDB.
- Início de downloads por links magnet.
- Acompanhamento do progresso, velocidade e quantidade de peers em tempo real.
- Organização dos downloads em uma interface simples.

Tecnologias:
- Python
- FastAPI
- PyQt5
- libtorrent
- Requests

Como usar:

1) Instale as dependências: "pip install -r requirements.txt"

2) Crie um arquivo `fonte1.json` seguindo este modelo:

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

3) Adicione sua chave da SteamGridDB no arquivo backend.py:
- API_KEY = "SUA_API_KEY"
- Execute o backend: "uvicorn backend:app --reload"
- Execute a interface: "python main.py"

Aviso:
Este repositório contém apenas o código-fonte do projeto. Nenhum arquivo magnet, catálogo de downloads ou conteúdo protegido por direitos autorais é distribuído junto com a aplicação.


