import os
import requests

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar
)


class DownloadCard(QWidget):
    def __init__(self, id_download, titulo):
        super().__init__()

        self.id = id_download
        self.titulo = titulo

        self.setStyleSheet("""
            QWidget{
                background:#1e1e1e;
                border-radius:8px;
            }

            QLabel{
                color:white;
                border:none;
                font-size:13px;
            }

            QPushButton{
                background:#2d89ef;
                color:white;
                border:none;
                padding:6px;
                border-radius:5px;
            }

            QPushButton:hover{
                background:#4da3ff;
            }

            QProgressBar{
                border:1px solid #333;
                border-radius:5px;
                text-align:center;
                background:#121212;
            }

            QProgressBar::chunk{
                background:#2d89ef;
            }
        """)

        layout = QVBoxLayout()

        self.lblTitulo = QLabel(titulo)
        self.lblTitulo.setWordWrap(True)

        self.barra = QProgressBar()
        self.barra.setValue(0)

        self.lblPorcentagem = QLabel("0%")
        self.lblEstado = QLabel("Iniciando...")
        self.lblVelocidade = QLabel("Velocidade: 0 KB/s")
        self.lblPeers = QLabel("Peers: 0")

        botoes = QHBoxLayout()

        self.btnCancelar = QPushButton("Cancelar")
        self.btnAbrir = QPushButton("Abrir Pasta")

        self.btnAbrir.setEnabled(False)

        botoes.addWidget(self.btnCancelar)
        botoes.addWidget(self.btnAbrir)

        layout.addWidget(self.lblTitulo)
        layout.addWidget(self.barra)
        layout.addWidget(self.lblPorcentagem)
        layout.addWidget(self.lblEstado)
        layout.addWidget(self.lblVelocidade)
        layout.addWidget(self.lblPeers)
        layout.addLayout(botoes)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar)
        self.timer.start(1000)

        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnAbrir.clicked.connect(self.abrir_pasta)

    def formatar_velocidade(self, velocidade):

        if velocidade < 1024:
            return f"{velocidade} B/s"

        if velocidade < 1024 * 1024:
            return f"{velocidade/1024:.1f} KB/s"

        return f"{velocidade/(1024*1024):.2f} MB/s"

    def traduzir_estado(self, estado):

        estados = {
            "queued": "Na fila",
            "checking": "Verificando",
            "downloading metadata": "Baixando metadados",
            "downloading": "Baixando",
            "finished": "Finalizado",
            "seeding": "Enviando",
            "allocating": "Preparando arquivos",
            "checking fastresume": "Verificando"
        }

        estado = estado.lower()

        for chave in estados:
            if chave in estado:
                return estados[chave]

        return estado

    def atualizar(self):

        try:

            resposta = requests.get(
                f"http://127.0.0.1:8000/status/{self.id}",
                timeout=5
            )

            dados = resposta.json()

            if "error" in dados:
                return

            progresso = int(dados["progress"])

            self.barra.setValue(progresso)
            self.lblPorcentagem.setText(f"{progresso}%")

            self.lblEstado.setText(
                "Estado: " +
                self.traduzir_estado(dados["state"])
            )

            self.lblVelocidade.setText(
                "Velocidade: " +
                self.formatar_velocidade(
                    dados["download_rate"]
                )
            )

            self.lblPeers.setText(
                f"Peers: {dados['peers']}"
            )

            if progresso >= 100:

                self.timer.stop()

                self.lblEstado.setText("✔ Download concluído")

                self.btnAbrir.setEnabled(True)

                self.btnCancelar.setEnabled(False)

        except Exception:
            pass

    def cancelar(self):

    # envia o pedido para o backend cancelar o download
        try:

            requests.get(
                f"http://127.0.0.1:8000/cancelar/{self.id}",
                timeout=5
            )

        except Exception:
            pass

         # para a atualização do card
        self.timer.stop()

        self.lblEstado.setText("Cancelado")

        self.btnCancelar.setEnabled(False)

        self.btnAbrir.setEnabled(False)

    def abrir_pasta(self):

        pasta = os.path.abspath(f"./downloads/{self.id}")

        os.startfile(pasta)