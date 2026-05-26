import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._airports = DAO.getAllAirports()
        self._grafo = nx.Graph()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGrafo(self,nMin):
        nodes=DAO.getAllNodes(nMin,self._idMapAirports)
        self._grafo.add_nodes_from(nodes)
        self.addEdges()


    def addEdges(self):
        allTratte=DAO.getAllEdgesV1(self._idMapAirports)
        #queste tratte hanno 2 problemi:
        # 1  ho archi diretti ed inversi
        # 2 ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._grafo and t.aeroportoA in self._grafo:
                if self._grafo.has_edge(t.aeroportoP, t.aeroportoA):
                    self._grafo[t.aeroportoP][t.aeroportoA]["weight"]+=t.peso
                else:
                    self._grafo.add_edge(t.aeroportoP,t.aeroportoA, weight=t.peso)



    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


