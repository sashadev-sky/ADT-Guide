import random
import math
import tkinter as tk


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('random_trees')
        self.window.protocol('WM_DELETE_WINDOW', self.kill_callback)
        self.window.geometry('400x400')

        frame = tk.Frame(self.window)
        frame.pack(side=tk.TOP, fill=tk.X)
        label = tk.Label(frame, text='Seed:')
        label.pack(padx=5, pady=5, side=tk.LEFT)
        self.seed_entry = tk.Entry(frame, width=8, justify=tk.RIGHT)
        self.seed_entry.pack(padx=5, pady=5, side=tk.LEFT)
        self.seed_entry.insert(0, '0')
        go_button = tk.Button(frame, text='Go', width=8, command=self.go)
        go_button.pack(padx=5, pady=5, side=tk.LEFT)
        random_button = tk.Button(frame, text='Random', width=8, command=self.random)
        random_button.pack(padx=5, pady=5, side=tk.LEFT)

        self.canvas = tk.Canvas(self.window, relief=tk.RIDGE, bd=5, bg='white')
        self.canvas.pack(padx=5, pady=(0,5), side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind some keys.
        self.window.bind('<Return>', (lambda e, button=go_button: go_button.invoke()))

        # Force focus so Alt+F4 closes this window and not the Python shell.
        self.seed_entry.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        self.window.destroy()

    def go(self):
        """Draw a tree that uses the entered seed value."""
        seed = int(self.seed_entry.get())
        self.draw_tree(seed)

    def random(self):
        """Draw a tree that uses a random seed value."""
        random.seed()
        seed = random.randint(0, 1000000)
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, f"{seed}")
        self.draw_tree(seed)

    def draw_tree(self, seed):
        """Use the given seed to draw a random tree."""
        # Initialize the random number generator.
        random.seed(seed)

        # Draw the tree.
        self.canvas.delete(tk.ALL)
        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() - 5
        thickness = 5
        length = (y * random.randint(20, 30) / 100)
        angle = -math.pi / 2
        self.draw_branch(thickness, length, x, y, angle)

    def draw_branch(self, thickness, length, x, y, angle):
        """Draw a branch and then recursively draw child branches."""
        # See where this branch ends.
        x1 = x + length * math.cos(angle)
        y1 = y + length * math.sin(angle)

        # Draw the branch.
        self.canvas.create_line(x, y, x1, y1, width=thickness)

        # Draw branches off of this one.
        num_branches = random.randint(2, 5)
        for i in range(num_branches):
            scale = random.randint(50, 75) / 100
            new_thickness = thickness * scale
            new_length = length * scale

            # Don't draw if it's too short.
            if new_length > 5:
                new_angle = angle + random.randint(-60, 61) * math.pi / 180
                self.draw_branch(new_thickness, new_length, x1, y1, new_angle)


if __name__ == '__main__':
    app = App()
