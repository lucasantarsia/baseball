from model.model import Model

mymodel = Model()

mymodel.getTeamsOfYear(2015)
mymodel.buildGraph(2015)
mymodel.printGraphDetails()

v0 = list(mymodel._grafo.nodes)[2]

vicini = mymodel.getSortedNeighbors(v0)

for v in vicini:
    print(v[1], v[0])

path = mymodel.getPercorso(v0)
print(path)
print(len(path))
