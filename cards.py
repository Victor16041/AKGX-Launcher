import requests

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QMessageBox
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CardJogo(QWidget):

    def __init__(
        self,
        jogo,
        tela_downloads=None,
        abas=None
    ):
        super().__init__()

        # guardando as informações do jogo
        self.jogo = jogo
        self.tela_downloads = tela_downloads
        self.abas = abas

        # tamanho do card
        self.setFixedSize(220, 380)

        # estilo do card
        self.setStyleSheet("""
            QWidget{
                background:#1e1e1e;
                border-radius:8px;
            }

            QLabel{
                color:white;
                border:none;
            }

            QPushButton{
                background:#2d89ef;
                color:white;
                border:none;
                padding:8px;
                border-radius:5px;
            }

            QPushButton:hover{
                background:#4da3ff;
            }
        """)

        layout = QVBoxLayout()

        # imagem da capa do jogo
        self.imagem = QLabel()
        self.imagem.setFixedSize(200,300)
        self.imagem.setAlignment(Qt.AlignCenter)

        # nome do jogo
        self.nome = QLabel(jogo["titulo"])
        self.nome.setAlignment(Qt.AlignCenter)
        self.nome.setWordWrap(True)
        self.nome.setFixedHeight(40)

        # botão de download
        self.botao = QPushButton("Download")
        self.botao.clicked.connect(self.baixar)

        try:

            # verificando se o jogo possui capa
            if jogo["capa"]:

                # baixando a imagem da capa
                dados = requests.get(
                    jogo["capa"],
                    timeout=10
                ).content

                pixmap = QPixmap()
                pixmap.loadFromData(dados)

                # colocando a imagem no card
                self.imagem.setPixmap(
                    pixmap.scaled(
                        200,
                        300,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                )

            else:

                self.imagem.setText("sem capa")

        except Exception:

            self.imagem.setText("sem capa")

        layout.addWidget(self.imagem)
        layout.addWidget(self.nome)
        layout.addWidget(self.botao)

        self.setLayout(layout)


    def baixar(self):

        try:

            # enviando pedido para o backend iniciar o download
            resposta = requests.get(
                f"http://127.0.0.1:8000{self.jogo['download']}",
                timeout=10
            )

            dados = resposta.json()

            # verificando se ocorreu algum erro
            if "error" in dados:

                QMessageBox.warning(
                    self,
                    "erro",
                    dados["error"]
                )

                return


            # alterando o botão depois de iniciar
            self.botao.setText("baixando...")
            self.botao.setEnabled(False)


            # adicionando o download na tela de downloads
            if self.tela_downloads:

                self.tela_downloads.adicionar_download(
                    dados["id"],
                    dados["titulo"]
                )


            # mudando para a aba de downloads
            if self.abas:

                self.abas.setCurrentIndex(1)
 

        except Exception as e:

            QMessageBox.critical(
                self,
                "erro",
                str(e)
            )



class ListaCards(QScrollArea):

    def __init__(
        self,
        tela_downloads=None,
        abas=None
    ):
        super().__init__()

        self.tela_downloads = tela_downloads
        self.abas = abas

        # área onde os cards ficam
        self.container = QWidget()

        self.grid = QGridLayout()
        self.container.setLayout(self.grid)

        self.setWidget(self.container)
        self.setWidgetResizable(True)


    def carregar(self, jogos):

        # removendo cards antigos antes de carregar novos
        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()


        linha = 0
        coluna = 0


        # criando um card para cada jogo encontrado
        for jogo in jogos:

            card = CardJogo(
                jogo=jogo,
                tela_downloads=self.tela_downloads,
                abas=self.abas
            )


            self.grid.addWidget(
                card,
                linha,
                coluna
            )


            coluna += 1


            # depois de 4 cards, passa para a próxima linha
            if coluna >= 4:

                coluna = 0
                linha += 1


        self.container.adjustSize()