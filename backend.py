import os
import json
from urllib.parse import quote

import libtorrent as lt
import requests
from fastapi import FastAPI

# criando a aplicação do fastapi
app = FastAPI()

# chave da api da steamgriddb para buscar capas dos jogos
API_KEY = "SUA_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# carregando o arquivo com a lista de jogos
with open("fonte1.json", "r", encoding="utf-8") as f:
    fonte1 = json.load(f)

# pegando apenas a lista de downloads do arquivo json
downloads = fonte1["downloads"]

# pasta onde os downloads serão salvos
BASE_DIR = os.path.abspath("./downloads")
os.makedirs(BASE_DIR, exist_ok=True)

# criando a sessão do libtorrent
ses = lt.session()
ses.listen_on(6881, 6891)

# diminuindo os alertas do libtorrent
settings = ses.get_settings()
settings["alert_mask"] = 0
ses.apply_settings(settings)

# lista que guarda os downloads ativos
downloads_ativos = {}

def pegar_capa(nome):

    try:

        # procurando o jogo na steamgriddb
        resposta = requests.get(
            f"https://www.steamgriddb.com/api/v2/search/autocomplete/{quote(nome)}",
            headers=headers,
            timeout=10
        )

        print("busca:", nome)
        print("status busca:", resposta.status_code)
        print("resposta:", resposta.text[:300])


        if resposta.status_code != 200:
            return None


        dados = resposta.json().get("data", [])


        if not dados:
            print("nenhum jogo encontrado")
            return None


        game_id = dados[0]["id"]

        print("id encontrado:", game_id)


        # buscando capas
        resposta = requests.get(
            f"https://www.steamgriddb.com/api/v2/grids/game/{game_id}?limit=1",
            headers=headers,
            timeout=10
        )


        print("status capa:", resposta.status_code)
        print("resposta capa:", resposta.text[:300])


        if resposta.status_code != 200:
            return None


        dados = resposta.json().get("data", [])


        if not dados:
            print("nenhuma capa encontrada")
            return None


        print("capa encontrada:", dados[0])


        return dados[0]["thumb"]


    except Exception as e:

        print("erro:", e)
        return None

# pesquisa jogos pelo nome
@app.get("/buscar/{nome}")
def buscar(nome: str):
    resultado = []

    for i, jogo in enumerate(downloads):

        if nome.lower() in jogo["title"].lower():
            resultado.append({
                "id": i,
                "titulo": jogo["title"],
                "capa": pegar_capa(jogo["title"]),
                "download": f"/download/{i}",
                "status": f"/status/{i}"
            })

    return resultado

# inicia um download
@app.get("/download/{id}")
def iniciar_download(id: int):

    if id < 0 or id >= len(downloads):
        return {
            "error": "id inválido"
        }

    if str(id) in downloads_ativos:
        return {
            "status": "já baixando",
            "id": id,
            "titulo": downloads[id]["title"]
        }

    item = downloads[id]

    # pegando o link magnet
    magnet = item["uris"]

    if isinstance(magnet, list):
        magnet = magnet[0]

    # criando pasta do download
    pasta = os.path.join(
        BASE_DIR,
        str(id)
    )

    os.makedirs(pasta, exist_ok=True)

    params = {
        "save_path": pasta,
        "storage_mode": lt.storage_mode_t.storage_mode_allocate
    }

    # adicionando o download no libtorrent
    handle = lt.add_magnet_uri(
        ses,
        magnet,
        params
    )

    downloads_ativos[str(id)] = {
        "handle": handle,
        "titulo": item["title"],
        "pasta": pasta
    }

    return {
        "status": "iniciado",
        "id": id,
        "titulo": item["title"]
    }

# mostra o status de um download
@app.get("/status/{id}")
def status(id: int):

    if str(id) not in downloads_ativos:
        return {
            "error": "download não encontrado"
        }

    info = downloads_ativos[str(id)]
    handle = info["handle"]

    s = handle.status()

    estados = [
        "aguardando",
        "verificando",
        "baixando metadados",
        "baixando",
        "finalizado",
        "enviando",
        "preparando arquivos",
        "verificando dados salvos"
    ]

    estado = "desconhecido"

    try:
        estado = estados[int(s.state)]
    except Exception:
        pass

    return {
        "id": id,
        "titulo": info["titulo"],
        "progress": round(s.progress * 100, 2),
        "download_rate": s.download_rate,
        "upload_rate": s.upload_rate,
        "peers": s.num_peers,
        "state": estado,
        "save_path": info["pasta"]
    }

# lista todos os downloads ativos
@app.get("/downloads")
def listar_downloads():

    lista = []

    estados = [
        "aguardando",
        "verificando",
        "baixando metadados",
        "baixando",
        "finalizado",
        "enviando",
        "preparando arquivos",
        "verificando dados salvos"
    ]

    for id_download, info in downloads_ativos.items():

        handle = info["handle"]
        s = handle.status()

        try:
            estado = estados[int(s.state)]
        except Exception:
            estado = "desconhecido"

        lista.append({
            "id": int(id_download),
            "titulo": info["titulo"],
            "progress": round(s.progress * 100, 2),
            "download_rate": s.download_rate,
            "upload_rate": s.upload_rate,
            "peers": s.num_peers,
            "state": estado,
            "save_path": info["pasta"]
        })

    return lista

# cancela um download
@app.get("/cancelar/{id}")
def cancelar_download(id: int):

    info = downloads_ativos.get(str(id))

    if not info:
        return {
            "error": "download não encontrado"
        }

    try:
        ses.remove_torrent(info["handle"])

    except Exception as e:
        return {
            "error": str(e)
        }

    del downloads_ativos[str(id)]

    return {
        "status": "cancelado"
    }

# verifica se o backend está funcionando
@app.get("/")
def home():

    return {
        "status": "AKGX Launcher",
        "downloads_ativos": len(downloads_ativos)
    }