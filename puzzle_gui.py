import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("600x700")
        
        self.current_step = 0
        self.solution_path = []
        
        # Create main frames
        self.create_input_frame()
        self.create_board_frame()
        self.create_controls_frame()
        self.create_info_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Initial State Input", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Grid for input
        grid_frame = ttk.Frame(input_frame)
        grid_frame.pack(side="left", padx=10)
        
        ttk.Label(grid_frame, text="Enter initial board (0 for blank):").grid(row=0, column=0, columnspan=3, pady=5)
        
        self.entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(grid_frame, width=5, justify="center", font=("Arial", 14))
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # Set default solvable puzzle
        default = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        for i in range(3):
            for j in range(3):
                self.entries[i][j].insert(0, str(default[i][j]))
        
        # Algorithm selection
        algo_frame = ttk.Frame(input_frame)
        algo_frame.pack(side="left", padx=20)
        
        ttk.Label(algo_frame, text="Select Algorithm:").pack(anchor="w")
        
        self.algorithm = tk.StringVar(value="bfs")
        algorithms = [
            ("Breadth-First Search", "bfs"),
            ("Depth-First Search", "dfs"),
            ("Iterative Deepening DFS", "iddfs"),
            ("A* (Manhattan)", "astar_manhattan"),
            ("A* (Euclidean)", "astar_euclidean")
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm, 
                          value=value).pack(anchor="w")
        
        # Solve button
        ttk.Button(algo_frame, text="Solve Puzzle", command=self.solve_puzzle, 
                  style="Accent.TButton").pack(pady=10)
    
    def create_board_frame(self):
        board_frame = ttk.LabelFrame(self.root, text="Puzzle Board", padding=10)
        board_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Canvas for drawing the board
        self.canvas = tk.Canvas(board_frame, width=400, height=400, bg="white")
        self.canvas.pack()
        
    def create_controls_frame(self):
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        self.prev_button = ttk.Button(controls_frame, text="← Previous", 
                                      command=self.previous_step, state="disabled")
        self.prev_button.pack(side="left", padx=5)
        
        self.step_label = ttk.Label(controls_frame, text="Step: 0 / 0", 
                                    font=("Arial", 12, "bold"))
        self.step_label.pack(side="left", expand=True)
        
        self.next_button = ttk.Button(controls_frame, text="Next →", 
                                      command=self.next_step, state="disabled")
        self.next_button.pack(side="right", padx=5)
    
    def create_info_frame(self):
        info_frame = ttk.LabelFrame(self.root, text="Solution Info", padding=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_text = tk.Text(info_frame, height=4, wrap="word", font=("Arial", 10))
        self.info_text.pack(fill="x")
        self.info_text.config(state="disabled")
    
    def draw_board(self, board):
        self.canvas.delete("all")
        cell_size = 120
        margin = 20
        
        for i in range(3):
            for j in range(3):
                x1 = margin + j * cell_size
                y1 = margin + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Draw cell
                if board[i][j] == 0:
                    # Blank cell
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0e0e0", 
                                                outline="#999")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#4CAF50", 
                                                outline="#2E7D32", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, 
                                          text=str(board[i][j]), 
                                          font=("Arial", 36, "bold"), 
                                          fill="white")
    
    def solve_puzzle(self):
        # Get board from entries
        try:
            board = []
            for i in range(3):
                row = []
                for j in range(3):
                    val = int(self.entries[i][j].get())
                    if val < 0 or val > 8:
                        raise ValueError("Numbers must be 0-8")
                    row.append(val)
                board.append(row)
            
            # Validate all numbers 0-8 present
            nums = [board[i][j] for i in range(3) for j in range(3)]
            if sorted(nums) != list(range(9)):
                raise ValueError("Must use each number 0-8 exactly once")
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        
        # Build command
        cmd = ["./puzzle_solver_json.exe" if os.name == 'nt' else "./puzzle_solver_json", 
               self.algorithm.get()]
        for row in board:
            cmd.extend([str(x) for x in row])
        
        # Run solver
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                messagebox.showerror("Error", f"Solver failed:\n{result.stderr}")
                return
            
            # Parse JSON output
            data = json.loads(result.stdout)
            
            if "error" in data:
                messagebox.showerror("No Solution", data["error"])
                return
            
            # Store solution
            self.solution_path = data["path"]
            self.current_step = 0
            
            # Update info
            self.update_info(data)
            
            # Enable buttons
            self.update_buttons()
            
            # Draw initial board
            self.draw_board(self.solution_path[0])
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Timeout", "Solver took too long (>30s)")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Failed to parse output:\n{result.stdout}")
        except FileNotFoundError:
            messagebox.showerror("Error", 
                               "puzzle_solver_json executable not found!\n" +
                               "Please compile the C++ code first:\n" +
                               "Run 'make' in the project directory")
    
    def update_info(self, data):
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        
        info = f"Algorithm: {data['algorithm']}\n"
        info += f"Cost: {data['cost']} moves\n"
        info += f"Nodes Expanded: {data['nodes_expanded']}\n"
        info += f"Runtime: {data['runtime_ms']} ms"
        
        self.info_text.insert(1.0, info)
        self.info_text.config(state="disabled")
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_board(self.solution_path[self.current_step])
            self.update_buttons()
    
    def next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.draw_board(self.solution_path[self.current_step])
            self.update_buttons()
    
    def update_buttons(self):
        if not self.solution_path:
            self.prev_button.config(state="disabled")
            self.next_button.config(state="disabled")
            self.step_label.config(text="Step: 0 / 0")
            return
        
        self.step_label.config(text=f"Step: {self.current_step + 1} / {len(self.solution_path)}")
        
        if self.current_step <= 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")
        
        if self.current_step >= len(self.solution_path) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()