import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza=None
        self._choiceArrivo=None
        self._mapAeroportiDD = {}

    def handleAnalizza(self, e):
        cMinTxt=self._view._txtInCMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore numerico per numero minimo compagnie",
                color="red"))
            self._view.update_page()

            return
        try:
            cMin=int(cMinTxt)
            self._view.update_page()

        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore numerico intero per numero minimo compagnie",
                color="red"))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Inserire un valore numerico intero positivo per numero minimo compagnie",
                color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        nNodes, nEdges=self._model.getGraphDetails()
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato:",
            color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo creato contiene: {nNodes} nodi e {nEdges} archi",
            color="green"))
        self._view.update_page()

        allNodes=self._model.getAllNodes()
        self._fillDropdown(allNodes)



    def handleConnessi(self, e):
        print(f"choicePartenza: {self._choicePartenza}")
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione per usare questo metood occorre selezionare "
                        "un aeroporto di partenza",color="red"))
            self._view.update_page()

            return
        viciniT=self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(ft.Text(
                f"{v[0]} - peso: {v[1]}",color="green"
            ))
        self._view.update_page()


    def handleCerca(self,e):
        pass

    def handleTestConnessione(self,e):
        pass

    def _fillDropdown(self, allNodes):
        self._view._ddAeroportoP.options.clear()
        self._view._ddAeroportoA.options.clear()
        self._mapAeroportiDD.clear()

        for n in allNodes:
            self._mapAeroportiDD[n.IATA_CODE] = n

            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(
                    key=n.IATA_CODE,
                    text=f"{n.IATA_CODE} - {n.AIRPORT}"
                )
            )

            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(
                    key=n.IATA_CODE,
                    text=f"{n.IATA_CODE} - {n.AIRPORT}"
                )
            )

        self._view.update_page()

    def _choiceDDPartenza(self, e):
        codice = e.control.value
        self._choicePartenza = self._mapAeroportiDD[codice]
        print(f"Hai selezionato come aeroporto di partenza {self._choicePartenza}")

    def _choiceDDArrivo(self, e):
        codice = e.control.value
        self._choiceArrivo = self._mapAeroportiDD[codice]
        print(f"Hai selezionato come aeroporto di partenza {self._choiceArrivo}")

