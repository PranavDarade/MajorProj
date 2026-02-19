import networkx as nx
from lxml import etree

# Create directed graph
G = nx.DiGraph()

# Parse SUMO net.xml
tree = etree.parse("mapL.net.xml")
root = tree.getroot()

# Add junctions (nodes)
for junction in root.findall("junction"):
    node_id = junction.get("id")

    # Skip internal junctions
    if node_id.startswith(":"):
        continue

    x = float(junction.get("x"))
    y = float(junction.get("y"))
    jtype = junction.get("type")

    G.add_node(
        node_id,
        x=x,
        y=y,
        type=jtype
    )

print("Nodes added:", G.number_of_nodes())

# Add edges (roads)
for edge in root.findall("edge"):
    edge_id = edge.get("id")

    # Skip internal edges
    if edge_id.startswith(":"):
        continue

    from_node = edge.get("from")
    to_node = edge.get("to")

    lanes = edge.findall("lane")
    if not lanes:
        continue

    num_lanes = len(lanes)

    lane = lanes[0]
    length = float(lane.get("length"))
    speed = float(lane.get("speed"))
    width = float(lane.get("width", 3.5))  # default width

    G.add_edge(
        from_node,
        to_node,
        edge_id=edge_id,
        length=length,
        speed=speed,
        lanes=num_lanes,
        width=width
    )

print("Edges added:", G.number_of_edges())
nx.write_graphml(G, "borough.graphml")
list(G.nodes(data=True))[:3]
list(G.edges(data=True))[:3]