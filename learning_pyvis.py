from pyvis.network import Network

# 1. Create a Network object
# You can set options for the entire network here, like background color, font color, etc.
# 'notebook=True' is useful for displaying directly in Jupyter notebooks.
net = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")

# 2. Add nodes
# Each node needs a unique ID. You can also add a 'label' for display,
# and other attributes like 'color', 'size', 'title' (for tooltips), etc.
net.add_node(1, label="Node 1", color="red", title="This is the first node")
net.add_node(2, label="Node 2", size=30)
net.add_node(3, label="Node 3", shape="square")

# 3. Add edges
# Edges connect two nodes by their IDs. You can also add 'weight' (for thickness),
# 'title' (for edge tooltips), 'color', etc.
net.add_edge(1, 2, weight=5, title="Connection A-B")
net.add_edge(2, 3, color="green")
net.add_edge(1, 3) # Default weight and color

# 4. (Optional) Customize physics and interactions
# Pyvis uses a physics engine for layout. You can enable/disable it
# and fine-tune its parameters.
net.toggle_physics(True)
# net.set_edge_smoothness('continuous') # Other options like 'dynamic', 'horizontal', etc.
# net.set_node_smoothness(False)

# 5. Generate and save the HTML file
# This creates an HTML file that contains your interactive graph.
# 
net.show_buttons()


net.show("my_basic_graph.html" , notebook=False)

# In a Streamlit app, you'd use st.components.v1.html to embed the HTML
# as shown in your example code.