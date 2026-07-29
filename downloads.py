from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea
)

from download_card import DownloadCard


class TelaDownloads(QScrollArea):

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        # criando o container dos downloads
        self.container = QWidget()

        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        self.setWidget(self.container)

        # guardando os downloads que estão na tela
        self.downloads = {}

        # mensagem quando não existe nenhum download
        self.vazio = QLabel(
            "Nenhum download em andamento."
        )

        self.vazio.setStyleSheet("""
            QLabel{
                color:gray;
                font-size:18px;
                padding:30px;
            }
        """)

        self.layout.addWidget(self.vazio)

        # deixa os cards sempre no topo
        self.layout.addStretch()


    def adicionar_download(self, id_download, titulo):

        # evita adicionar o mesmo download duas vezes
        if id_download in self.downloads:
            return


        # remove a mensagem de lista vazia
        if self.vazio.parent():

            self.layout.removeWidget(
                self.vazio
            )

            self.vazio.deleteLater()


        # criando o card do download
        card = DownloadCard(
            id_download=id_download,
            titulo=titulo
        )


        self.downloads[id_download] = card


        # adicionando o card na lista
        self.layout.insertWidget(
            self.layout.count() - 1,
            card
        )


    def remover_download(self, id_download):

        # verifica se o download existe
        if id_download not in self.downloads:
            return


        card = self.downloads[id_download]


        # removendo o card da tela
        self.layout.removeWidget(card)

        card.deleteLater()


        del self.downloads[id_download]


        # caso não tenha mais downloads, mostra a mensagem
        if len(self.downloads) == 0:

            self.vazio = QLabel(
                "Nenhum download em andamento."
            )

            self.vazio.setStyleSheet("""
                QLabel{
                    color:gray;
                    font-size:18px;
                    padding:30px;
                }
            """)

            self.layout.insertWidget(
                0,
                self.vazio
            )


    def limpar(self):

        # removendo todos os cards da tela
        for card in self.downloads.values():

            card.deleteLater()


        self.downloads.clear()


        # criando novamente a mensagem de lista vazia
        self.vazio = QLabel(
            "Nenhum download em andamento."
        )

        self.vazio.setStyleSheet("""
            QLabel{
                color:gray;
                font-size:18px;
                padding:30px;
            }
        """)


        self.layout.insertWidget(
            0,
            self.vazio
        )