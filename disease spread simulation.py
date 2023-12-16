import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter as tk

# Function to initialize the graph with nodes and edges
def initialize_graph(num_nodes, avg_degree):
    if num_nodes % 2 != 0 and avg_degree % 2 != 0:
        num_nodes += 1
    G = nx.random_regular_graph(avg_degree, num_nodes)
    for node in G.nodes():
        G.nodes[node]["color"] = "healthy"
    return G


# Function to infect a random node
def infect_node(G):
    healthy_nodes = [node for node in G.nodes() if G.nodes[node]["color"] == "healthy"]
    if len(healthy_nodes) > 0:
        node = random.choice(healthy_nodes)
        G.nodes[node]["color"] = "infected"
    print("A random node has been infected.")


# Function to find a spanning tree
def find_spanning_tree(G):
    tree = nx.minimum_spanning_tree(G)
    print("A spanning tree has been created.")
    return tree


# Function to simulate the disease spreading
def simulate_spread(G, num_iterations):
    infected_count = []
    for _ in range(num_iterations):
        infected_nodes = [node for node in G.nodes() if G.nodes[node]["color"] == "infected"]
        infected_count.append(len(infected_nodes))

        for node in infected_nodes:
            neighbors = list(G.neighbors(node))
            susceptible_neighbors = [n for n in neighbors if G.nodes[n]["color"] == "healthy"]
            for neighbor in susceptible_neighbors:
                if random.random() < 0.5:  # Probability of transmission
                    G.nodes[neighbor]["color"] = "infected"
        print("Disease spread simulated for one iteration.")
    return infected_count


# Function to visualize the graph and display node counts
def visualize_graph(G):
    if G is not None:
        healthy_count = sum(1 for node in G.nodes() if G.nodes[node]["color"] == "healthy")
        infected_count = sum(1 for node in G.nodes() if G.nodes[node]["color"] == "infected")

        print("Healthy nodes:", healthy_count)
        print("Infected nodes:", infected_count)

        pos = nx.spring_layout(G)
        colors = ["green" if G.nodes[node]["color"] == "healthy" else "red" for node in G.nodes()]
        plt.figure(figsize=(8, 6))  # Set a fixed size for the figure
        nx.draw(G, pos, node_color=colors, with_labels=True, node_size=500)
        plt.show()
    else:
        print("No graph available.")


# Function to handle button click for each menu option
def handle_menu_choice(choice):
    global graph, spanning_tree
    if choice == "1":
        num_nodes = int(num_nodes_entry.get())
        avg_degree = int(avg_degree_entry.get())
        graph = initialize_graph(num_nodes, avg_degree)
        print("Graph has been initialized.")

    elif choice == "2":
        if graph is not None:
            spanning_tree = find_spanning_tree(graph)
        else:
            print("Please initialize the graph first.")

    elif choice == "3":
        if spanning_tree is not None:
            infect_node(spanning_tree)
        else:
            print("Please create a spanning tree first.")

    elif choice == "4":
        if spanning_tree is not None:
            num_iterations = int(num_iterations_entry.get())
            infected_count = simulate_spread(spanning_tree, num_iterations)
            print("Disease spread simulation completed.")

    elif choice == "5":
        visualize_graph(spanning_tree)

    print()  # Add an empty line for better readability


# Create the main window
window = tk.Tk()
window.title("Disease Spread Simulation")
window.configure(bg="#F9F6FF")  # Set background color to a lighter shade

# Create labels and entry fields for user input
label_style = "Helvetica 12 bold"  # Custom label font style
entry_style = "Helvetica 12"  # Custom entry field font style
label_bg = "#F9F6FF"  # Custom label background color
entry_bg = "#FFFFFF"  # Custom entry field background color

num_nodes_label = tk.Label(window, text="Number of Nodes:", bg=label_bg, font=label_style)
num_nodes_entry = tk.Entry(window, bg=entry_bg, font=entry_style)
avg_degree_label = tk.Label(window, text="Average Degree:", bg=label_bg, font=label_style)
avg_degree_entry = tk.Entry(window, bg=entry_bg, font=entry_style)
num_iterations_label = tk.Label(window, text="Number of Iterations:", bg=label_bg, font=label_style)
num_iterations_entry = tk.Entry(window, bg=entry_bg, font=entry_style)

# Create buttons for each menu option with enhanced styling
button_style = "Helvetica 12 bold"  # Custom button font style
button_bg = "#D4C3FF"  # Custom button background color
button_fg = "#000000"  # Custom button text color

initialize_button = tk.Button(window, text="Initialize Graph", command=lambda: handle_menu_choice("1"), bg=button_bg,
                              fg=button_fg, font=button_style, borderwidth=2)
create_tree_button = tk.Button(window, text="Create Spanning Tree", command=lambda: handle_menu_choice("2"),
                               bg=button_bg, fg=button_fg, font=button_style, borderwidth=2)
infect_node_button = tk.Button(window, text="Infect Initial Node", command=lambda: handle_menu_choice("3"),
                               bg=button_bg, fg=button_fg, font=button_style, borderwidth=2)
simulate_button = tk.Button(window, text="Simulate Disease Spread", command=lambda: handle_menu_choice("4"),
                            bg=button_bg, fg=button_fg, font=button_style, borderwidth=2)
visualize_button = tk.Button(window, text="Visualize Graph", command=lambda: handle_menu_choice("5"),
                             bg=button_bg, fg=button_fg, font=button_style, borderwidth=2)
exit_button = tk.Button(window, text="Exit", command=window.destroy, bg=button_bg, fg=button_fg, font=button_style,
                        borderwidth=2)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)

# Grid layout for labels and entry fields
num_nodes_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
num_nodes_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
avg_degree_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
avg_degree_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
num_iterations_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
num_iterations_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Grid layout for buttons
initialize_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
create_tree_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
infect_node_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
simulate_button.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
visualize_button.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
exit_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

# Center the menu and buttons
window.grid_rowconfigure(6, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the main event loop
window.mainloop()
