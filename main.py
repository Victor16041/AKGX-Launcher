import sys
import requests

from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTabWidget
)

from cards import ListaCards
from downloads import TelaDownloads


class BuscaThread(QThread):

    terminou = pyqtSignal(list)
    erro = pyqtSignal(str)

    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def run(self):

        try:

            # buscando os jogos no backend
            resposta = requests.get(
                f"http://127.0.0.1:8000/buscar/{self.nome}",
                timeout=30
            )

            self.terminou.emit(
                resposta.json()
            )

        except Exception as e:

            self.erro.emit(
                str(e)
            )


class Janela(QWidget):

    def __init__(self):

        super().__init__()

        # configurações da janela
        self.setWindowTitle("AKGX Launcher")
        self.resize(1300, 750)

        self.setStyleSheet("""
            QWidget{
                background:#121212;
                color:white;
                font-size:14px;
            }

            QLineEdit{
                padding:10px;
                background:#1e1e1e;
                border:1px solid #333;
                border-radius:5px;
            }

            QPushButton{
                background:#2d89ef;
                color:white;
                border:none;
                padding:10px;
                border-radius:5px;
            }

            QPushButton:hover{
                background:#4da3ff;
            }

            QTabWidget::pane{
                border:none;
            }

            QTabBar::tab{
                background:#1e1e1e;
                padding:12px;
                width:150px;
            }

            QTabBar::tab:selected{
                background:#2d89ef;
            }
        """)

        layout_principal = QVBoxLayout()

        self.abas = QTabWidget()

        self.abaPesquisa = QWidget()
        self.abaDownloads = TelaDownloads()

        self.abas.addTab(self.abaPesquisa, "Pesquisar")
        self.abas.addTab(self.abaDownloads, "Downloads")

        layoutPesquisa = QVBoxLayout()

        barra = QHBoxLayout()

        self.pesquisa = QLineEdit()
        self.pesquisa.setPlaceholderText("Pesquisar jogo...")

        self.botao = QPushButton("Buscar")

        barra.addWidget(self.pesquisa)
        barra.addWidget(self.botao)

        self.loading = QLabel("")
        self.loading.setAlignment(Qt.AlignCenter)
        self.loading.hide()

        self.loading.setStyleSheet("""
            QLabel{
                color:#4da3ff;
                font-size:34px;
                font-weight:bold;
                padding:20px;
            }
        """)

        self.cards = ListaCards()

        layoutPesquisa.addLayout(barra)
        layoutPesquisa.addWidget(self.loading)
        layoutPesquisa.addWidget(self.cards)

        self.abaPesquisa.setLayout(layoutPesquisa)

        layout_principal.addWidget(self.abas)

        self.setLayout(layout_principal)

        self.botao.clicked.connect(self.buscar)
        self.pesquisa.returnPressed.connect(self.buscar)

        self.pontos = 1

        self.timer = QTimer()
        self.timer.timeout.connect(self.animar_loading)


    def animar_loading(self):

        self.loading.setText(
            "CARREGANDO" + "." * self.pontos
        )

        self.pontos += 1

        if self.pontos > 3:
            self.pontos = 1


    def buscar(self):

        nome = self.pesquisa.text().strip()

        if not nome:
            return

        # limpa resultados antigos
        self.cards.carregar([])

        self.botao.setEnabled(False)
        self.pesquisa.setEnabled(False)

        self.loading.show()

        self.pontos = 1
        self.animar_loading()

        self.timer.start(400)

        self.thread = BuscaThread(nome)

        self.thread.terminou.connect(
            self.finalizar_busca
        )

        self.thread.erro.connect(
            self.erro_busca
        )

        self.thread.start()


    def finalizar_busca(self, jogos):

        self.timer.stop()

        self.loading.hide()

        self.botao.setEnabled(True)
        self.pesquisa.setEnabled(True)

        # passando a tela de downloads para os cards
        self.cards.tela_downloads = self.abaDownloads

        # carregando os resultados
        self.cards.carregar(jogos)


    def erro_busca(self, erro):

        self.timer.stop()

        self.loading.hide()

        self.botao.setEnabled(True)
        self.pesquisa.setEnabled(True)

        print("erro:", erro)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    janela = Janela()
    janela.show()

    sys.exit(app.exec_())