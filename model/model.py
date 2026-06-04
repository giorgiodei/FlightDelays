import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirport={}
        for a in self._airports:
            self._idMapAirport[a.ID]=a
            #CON QUESTO, IN OGNI METODO DEL MIO MODELLO,
            # AVRO UNA MAPPA CHE POSSO UTILIZZARE PER RECUPERARE L'OGGETTO
            # DI TIPO MODELLO A PARTIRE DALLA SUA CHIAVE PRIMARIA

    def buildGraph(self,nMin):
        nodes=DAO.getAllNodes(nMin, self._idMapAirport)
        self._graph.add_nodes_from(nodes)
        self.addEdges()


    def getAllNodes(self):
        return sorted(list(self._graph.nodes()), key=lambda a: a.IATA_CODE)

    def getGraphDetails(self):
        return len(self._graph.nodes()), len(self._graph.edges())


    def addEdges(self):
        allTratte=DAO.getAllEdgesv1(self._idMapAirport)
        #queste tratte hanno 2 problemi:
        #i) ho archi diretti e inversi,
        #ii) ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:                 #allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"]+=t.peso
                else:
                    self._graph.add_edge(t.aeroportoP,t.aeroportoA, weight=t.peso)



    def getViciniOrdinati(self,source): #restituisce tutti i vicini di source ordinari per peso dell'arco che collega source al vicino

        vicini=self._graph.neighbors(source)
        viciniT=[]
        for v in vicini:
            viciniT.append((v, self._graph[source][v]["weight"]))
        viciniT.sort(key=lambda x: x[1])
        return viciniT





