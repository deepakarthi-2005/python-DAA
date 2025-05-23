import tkinter as tk
import random
import time
import math

# --------- Matching Algorithm (Divide and Conquer) ---------
def partition(arr, pivot, compare):
    smaller, equal, larger = [], [], []
    for item in arr:
        result = compare(item, pivot)
        if result < 0:
            smaller.append(item)
        elif result > 0:
            larger.append(item)
        else:
            equal.append(item)
    return smaller, equal, larger

def match_nuts_and_bolts(nuts, bolts, compare):
    if len(nuts) <= 1:
        return nuts, bolts

    pivot_bolt = random.choice(bolts)
    small_nuts, equal_nuts, large_nuts = partition(nuts, pivot_bolt, compare)

    if not equal_nuts:
        raise ValueError("No matching nut found for the pivot bolt")

    pivot_nut = equal_nuts[0]
    small_bolts, _, large_bolts = partition(bolts, pivot_nut, compare)

    left_nuts, left_bolts = match_nuts_and_bolts(small_nuts, small_bolts, compare)
    right_nuts, right_bolts = match_nuts_and_bolts(large_nuts, large_bolts, compare)

    return left_nuts + [pivot_nut] + right_nuts, left_bolts + [pivot_bolt] + right_bolts

# --------- GUI Class ---------
class NutsBoltsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nuts and Bolts Matcher")
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.n = 6
        self.nuts = random.sample(range(1, 100), self.n)
        self.bolts = self.nuts[:]
        random.shuffle(self.nuts)
        random.shuffle(self.bolts)

        self.nut_rects = []
        self.bolt_rects = []
        self.nut_texts = []
        self.bolt_texts = []
        self.nut_coords = []
        self.bolt_coords = []
        self.connection_lines = []
        self.step_counter = 0
        
        self.draw_elements()
        self.match_button = tk.Button(root, text="Match Nuts & Bolts", command=self.animate_matching)
        self.match_button.pack(pady=10)
        
        self.animation_speed = 500  # milliseconds between steps
        self.explanation_text = self.canvas.create_text(400, 450, text="", font=("Arial", 12), width=700)

    def draw_elements(self):
        self.canvas.delete("all")
        spacing = 800 // (self.n + 1)
        self.nut_coords = []
        self.bolt_coords = []
        self.nut_rects = []
        self.bolt_rects = []
        self.nut_texts = []
        self.bolt_texts = []
        self.connection_lines = []

        # Draw title
        self.canvas.create_text(400, 30, text="Nuts and Bolts Matching Algorithm", 
                              font=("Arial", 16, "bold"), fill="navy")

        for i, val in enumerate(self.nuts):
            x = (i + 1) * spacing
            y = 100
            rect = self.canvas.create_rectangle(x-15, y-20, x+15, y+20, 
                                             fill="orange", outline="darkorange", width=2)
            text = self.canvas.create_text(x, y, text=str(val), 
                                         font=("Arial", 10, "bold"), fill="black")
            self.nut_coords.append((x, y))
            self.nut_rects.append(rect)
            self.nut_texts.append(text)

        for i, val in enumerate(self.bolts):
            x = (i + 1) * spacing
            y = 300
            rect = self.canvas.create_rectangle(x-15, y-20, x+15, y+20, 
                                             fill="skyblue", outline="steelblue", width=2)
            text = self.canvas.create_text(x, y, text=str(val), 
                                         font=("Arial", 10, "bold"), fill="black")
            self.bolt_coords.append((x, y))
            self.bolt_rects.append(rect)
            self.bolt_texts.append(text)

        # Redraw explanation text
        self.explanation_text = self.canvas.create_text(400, 450, text="", 
                                                      font=("Arial", 12), width=700)

    def animate_move(self, item, start_pos, end_pos, steps=20):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        
        def move_step(step):
            if step < steps:
                new_x = start_x + dx * step
                new_y = start_y + dy * step
                self.canvas.coords(item, new_x-15, new_y-20, new_x+15, new_y+20)
                self.root.after(20, lambda: move_step(step + 1))
        
        move_step(0)

    def animate_size(self, item, start_size, end_size, steps=20):
        def size_step(step):
            if step < steps:
                size = start_size + (end_size - start_size) * (step / steps)
                x, y = self.canvas.coords(item)[:2]
                self.canvas.coords(item, x, y, x+size, y+size)
                self.root.after(20, lambda: size_step(step + 1))
        
        size_step(0)

    def create_connection_line(self, nut_pos, bolt_pos, color="gray"):
        line = self.canvas.create_line(nut_pos[0], nut_pos[1], bolt_pos[0], bolt_pos[1],
                                     fill=color, width=2, dash=(4, 4))
        self.connection_lines.append(line)
        return line

    def update_explanation(self, text):
        self.canvas.itemconfig(self.explanation_text, text=text)

    def animate_matching(self):
        self.match_button.config(state='disabled')
        self.step_counter = 0
        try:
            matched_nuts, matched_bolts = match_nuts_and_bolts(self.nuts, self.bolts, self.compare)
            
            # Calculate new positions
            spacing = 800 // (self.n + 1)
            new_nut_coords = []
            new_bolt_coords = []
            
            for i in range(self.n):
                x = (i + 1) * spacing
                new_nut_coords.append((x, 100))
                new_bolt_coords.append((x, 300))
            
            # Animate each pair
            for i in range(self.n):
                nut_idx = self.nuts.index(matched_nuts[i])
                bolt_idx = self.bolts.index(matched_bolts[i])
                
                # Schedule animations with delays
                self.root.after(i * self.animation_speed, 
                              lambda n=nut_idx, b=bolt_idx, i=i: self.animate_pair(n, b, i))
            
            # Update the arrays after animation
            self.root.after(self.n * self.animation_speed, 
                          lambda: self.finish_matching(matched_nuts, matched_bolts))
            
        except ValueError as e:
            self.canvas.create_text(400, 200, text=str(e), fill="red", font=("Arial", 14, "bold"))
            self.match_button.config(state='normal')

    def animate_pair(self, nut_idx, bolt_idx, new_idx):
        self.step_counter += 1
        spacing = 800 // (self.n + 1)
        new_x = (new_idx + 1) * spacing
        
        # Update explanation
        self.update_explanation(
            f"Step {self.step_counter}: Matching nut {self.nuts[nut_idx]} with bolt {self.bolts[bolt_idx]}\n"
            f"Using divide-and-conquer algorithm to find matching pairs"
        )
        
        # Create connection line
        line = self.create_connection_line(self.nut_coords[nut_idx], self.bolt_coords[bolt_idx])
        
        # Highlight the pair being matched
        self.canvas.itemconfig(self.nut_rects[nut_idx], fill="yellow", outline="gold")
        self.canvas.itemconfig(self.bolt_rects[bolt_idx], fill="lightgreen", outline="green")
        
        # Animate movement with size effect
        self.animate_move(self.nut_rects[nut_idx], self.nut_coords[nut_idx], (new_x, 100))
        self.animate_move(self.bolt_rects[bolt_idx], self.bolt_coords[bolt_idx], (new_x, 300))
        
        # Update text positions
        self.canvas.coords(self.nut_texts[nut_idx], new_x, 100)
        self.canvas.coords(self.bolt_texts[bolt_idx], new_x, 300)
        
        # Animate connection line
        def animate_line(step):
            if step < 20:
                progress = step / 20
                start_x, start_y = self.nut_coords[nut_idx]
                end_x, end_y = self.bolt_coords[bolt_idx]
                new_x1 = start_x + (new_x - start_x) * progress
                new_x2 = end_x + (new_x - end_x) * progress
                self.canvas.coords(line, new_x1, start_y, new_x2, end_y)
                self.root.after(20, lambda: animate_line(step + 1))
        
        animate_line(0)

    def finish_matching(self, matched_nuts, matched_bolts):
        self.nuts = matched_nuts
        self.bolts = matched_bolts
        self.canvas.create_text(400, 200, text="Matching Complete!", 
                              fill="green", font=("Arial", 14, "bold"))
        self.update_explanation(
            "Algorithm complete! All nuts and bolts have been matched.\n"
            "The divide-and-conquer approach efficiently matches pairs by recursively partitioning the sets."
        )
        self.match_button.config(state='normal')

    def compare(self, nut, bolt):
        if nut < bolt:
            return -1
        elif nut > bolt:
            return 1
        else:
            return 0

# --------- Main Program ---------
if __name__ == "__main__":
    root = tk.Tk()
    app = NutsBoltsGUI(root)
    root.mainloop()