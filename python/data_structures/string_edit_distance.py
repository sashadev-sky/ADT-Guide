from enum import Enum
import tkinter as tk


class Direction(Enum):
    """The direction we are traveling through the edit graph."""
    unknown = 0
    from_above = 1
    from_left = 2
    from_diagonal = 3


class Node:
    """A node in the edit graph."""
    def __init__(self):
        self.distance = 0
        self.direction = Direction.unknown

    def __str__(self):
        return f'{self.distance}:{self.direction}'

def make_edit_graph(string1, string2):
    """Create an edit graph for two strings."""
    # Make the edit graph array.
    num_cols = len(string1) + 1
    num_rows = len(string2) + 1
    nodes = [[Node() for col in range(num_cols)] for row in range(num_rows)]

    # Initialize the leftmost column.
    for r in range(num_rows):
        nodes[r][0].distance = r
        nodes[r][0].direction = Direction.from_above

    # Initialize the top row.
    for c in range(num_cols):
        nodes[0][c].distance = c
        nodes[0][c].direction = Direction.from_left

    # Fill in the rest of the array.
    for c in range(1, num_cols):
        # Fill in column c.
        for r in range(1, num_rows):
            # Fill in entry [r][c].
            # Check the three possible paths to here and pick the best.
            # From above.
            nodes[r][c].distance = nodes[r - 1][c].distance + 1
            nodes[r][c].direction = Direction.from_above

            # From the left.
            if nodes[r][c].distance > nodes[r][c - 1].distance + 1:
                nodes[r][c].distance = nodes[r][c - 1].distance + 1
                nodes[r][c].direction = Direction.from_left

            # Diagonal.
            if (string1[c - 1] == string2[r - 1]) and (nodes[r][c].distance > nodes[r - 1][c - 1].distance):
                nodes[r][c].distance = nodes[r - 1][c - 1].distance
                nodes[r][c].direction = Direction.from_diagonal

    return nodes


def display_results(string1, string2, nodes, text):
    """Display the changes in a text widget."""
    # Build a list of the moves from finish to start.
    num_rows = len(nodes)
    num_cols = len(nodes[0])
    r = num_rows - 1
    c = num_cols - 1

    # Make some fonts.
    text.tag_configure('keep_font', font=('Arial', 10), foreground='black')
    text.tag_configure('insert_font', font=('Arial', 10, 'underline'), foreground='blue')
    text.tag_configure('delete_font', font=('Arial', 10, 'overstrike'), foreground='red')
    text.delete('1.0', tk.END)

    # Continue until we reach the upper left corner.
    while (r > 0) or (c > 0):
        if nodes[r][c].direction == Direction.from_above:
            text.insert('1.0', string2[r - 1], 'insert_font')
            r -= 1
        elif nodes[r][c].direction == Direction.from_left:
            text.insert('1.0', string1[c - 1], 'delete_font')
            c -= 1
        elif nodes[r][c].direction == Direction.from_diagonal:
            text.insert('1.0', string2[r - 1], 'keep_font')
            r -= 1
            c -= 1


class App:
    def kill_callback(self):
        self.window.destroy()

    def __init__(self):
        # Make the widgets.
        self.window = tk.Tk()
        self.window.title('string_edit_distance')
        self.window.protocol('WM_DELETE_WINDOW', self.kill_callback)
        self.window.geometry('270x160')

        self.window.grid_columnconfigure(1, weight=1)

        label = tk.Label(self.window, text='Change This:')
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.from_entry = tk.Entry(self.window, width=1)
        self.from_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.from_entry.insert(tk.END, 'precipitation')

        label = tk.Label(self.window, text='Into This:')
        label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.to_entry = tk.Entry(self.window, width=1)
        self.to_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.to_entry.insert(tk.END, 'participation')

        compare_button = tk.Button(self.window, text='Compare', width=8, command=self.compare)
        compare_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        label = tk.Label(self.window, text='Distance:')
        label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.distance_entry = tk.Entry(self.window, width=5)
        self.distance_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        label = tk.Label(self.window, text='Edits:')
        label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.edits_text = tk.Text(self.window, width=1, height=1)
        self.edits_text.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

        # Bind some keys.
        self.window.bind('<Return>', (lambda e, button=compare_button: compare_button.invoke()))

        # Force focus so Alt+F4 closes this window and not the Python shell.
        self.from_entry.focus_force()
        self.window.mainloop()

    def compare(self):
        """Compare the strings."""
        # Build the edit graph.
        nodes = make_edit_graph(self.from_entry.get(), self.to_entry.get())

        # Display the edits.
        display_results(self.from_entry.get(), self.to_entry.get(), nodes, self.edits_text)

        # Display the edit distance.
        distance = nodes[len(nodes) - 1][len(nodes[0]) - 1].distance
        self.distance_entry.delete(0, tk.END)
        self.distance_entry.insert(tk.END, f"{distance}")


if __name__ == '__main__':
    app = App()

# app.root.destroy()
