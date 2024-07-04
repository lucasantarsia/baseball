import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        # self.fillDDYear() -> SBAGLIATO METTERLO QUI! Lo metto nel view

        self._selectedTeam = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un anno dal menù!"))
            self._view.update_page()
            return
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        nLen, eLen = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito da {nLen} nodi e {eLen} archi."))
        self._view.update_page()

    def handleDettagli(self, e):
        vicini = self._model.getSortedNeighbors(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam} con relativo peso dell'arco:"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        if self._selectedTeam is None:
            warnings.warn("Squadra non selezionata")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Squadra non selezionata"))
            self._view.update_page()
            return
        path = self._model.getPercorso(self._selectedTeam)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Percorso trovato:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p[0]} -- {p[1]}"))
        self._view.update_page()

    def handleDDYearSelection(self, e):
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che hanno "
                                                          f"giocato nel {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t,
                                                                    text=t.teamCode,
                                                                    on_click=self.readDDTeam))
        self._view.update_page()

    def readDDTeam(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeam called -- {self._selectedTeam}")

    def fillDDYear(self):
        years = self._model.getYears()
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        # map: prende come primo argomento una funzione, come secondo un iterable e applica la funzione ad ogni elemento della funzione

        # yearsDD = []
        # for y in years:
        #     yearsDD.append(ft.dropdown.Option(y))

        self._view._ddAnno.options = yearsDD
        self._view.update_page()
