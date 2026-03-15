import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_graphml("borough.graphml")

pos = {
    node: (float(data["x"]), float(data["y"]))
    for node, data in G.nodes(data=True)
}

plt.figure(figsize=(10, 10))
nx.draw(
    G,
    pos,
    node_size=1,
    edge_color="gray",
    width=0.2
)
plt.title("Chelsea Road Network")
plt.show()