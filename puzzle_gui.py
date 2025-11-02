import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f0f0")
        
        self.current_step = 0
        self.solution_path = []
        
        # Configure styles
        self.setup_styles()
        
        # Create main container with two columns
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Board and controls
        left_frame = tk.Frame(main_container, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right side - Input and info
        right_frame = tk.Frame(main_container, bg="#f0f0f0", width=400)
        right_frame.pack(side="right", fill="both", padx=(10, 0))
        right_frame.pack_propagate(False)
        
        self.create_board_section(left_frame)
        self.create_input_frame(right_frame)
        self.create_info_frame(right_frame)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure("Solve.TButton",
                       font=("Arial", 12, "bold"),
                       foreground="white",
                       background="#4CAF50",
                       borderwidth=0,
                       focuscolor="none",
                       padding=10)
        style.map("Solve.TButton",
                 background=[("active", "#45a049")])
        
        # Configure frame style
        style.configure("Card.TFrame",
                       background="white",
                       relief="flat")
        
        # Configure label style
        style.configure("Title.TLabel",
                       font=("Arial", 14, "bold"),
                       background="white",
                       foreground="#333")
        
        style.configure("Subtitle.TLabel",
                       font=("Arial", 11, "bold"),
                       background="white",
                       foreground="#666")
    
    def create_board_section(self, parent):
        # Board frame with nice border
        board_container = tk.Frame(parent, bg="white", highlightbackground="#ddd", 
                                  highlightthickness=1)
        board_container.pack(fill="both", expand=True)
        
        # Title
        title = tk.Label(board_container, text="🧩 Puzzle Board", 
                        font=("Arial", 16, "bold"), bg="white", fg="#333", pady=15)
        title.pack()
        
        # Board with arrow controls container
        board_with_controls = tk.Frame(board_container, bg="white")
        board_with_controls.pack(expand=True, pady=20)
        
        # Left arrow
        left_arrow_frame = tk.Frame(board_with_controls, bg="white")
        left_arrow_frame.pack(side="left", padx=20)
        
        self.left_arrow = tk.Canvas(left_arrow_frame, width=60, height=60, 
                                    bg="white", highlightthickness=0, cursor="hand2")
        self.left_arrow.pack()
        self.draw_arrow(self.left_arrow, "left", "disabled")
        self.left_arrow.bind("<Button-1>", lambda e: self.previous_step())
        
        # Canvas for drawing the board
        self.canvas = tk.Canvas(board_with_controls, width=400, height=400, 
                               bg="white", highlightthickness=0)
        self.canvas.pack(side="left")
        
        # Right arrow
        right_arrow_frame = tk.Frame(board_with_controls, bg="white")
        right_arrow_frame.pack(side="left", padx=20)
        
        self.right_arrow = tk.Canvas(right_arrow_frame, width=60, height=60, 
                                     bg="white", highlightthickness=0, cursor="hand2")
        self.right_arrow.pack()
        self.draw_arrow(self.right_arrow, "right", "disabled")
        self.right_arrow.bind("<Button-1>", lambda e: self.next_step())
        
        # Step counter below board
        self.step_label = tk.Label(board_container, text="Step: 0 / 0", 
                                   font=("Arial", 14, "bold"), bg="white", fg="#666", pady=15)
        self.step_label.pack()
    
    def draw_arrow(self, canvas, direction, state="normal"):
        canvas.delete("all")
        
        if state == "disabled":
            fill_color = "#cccccc"
            outline_color = "#aaaaaa"
        else:
            fill_color = "#4CAF50"
            outline_color = "#2E7D32"
        
        if direction == "left":
            # Left arrow
            points = [45, 30, 20, 30, 20, 20, 5, 30, 20, 40, 20, 30]
            canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2)
        else:
            # Right arrow
            points = [15, 30, 40, 30, 40, 20, 55, 30, 40, 40, 40, 30]
            canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2)
    
    def create_input_frame(self, parent):
        input_container = tk.Frame(parent, bg="white", highlightbackground="#ddd", 
                                  highlightthickness=1)
        input_container.pack(fill="both", padx=0, pady=(0, 15))
        
        # Title
        title = tk.Label(input_container, text="⚙️ Setup", 
                        font=("Arial", 16, "bold"), bg="white", fg="#333", pady=15)
        title.pack()
        
        content = tk.Frame(input_container, bg="white")
        content.pack(fill="both", padx=20, pady=(0, 20))
        
        # Grid input section
        ttk.Label(content, text="Initial Board State", style="Subtitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        grid_frame = tk.Frame(content, bg="white")
        grid_frame.pack(pady=(0, 20))
        
        self.entries = []
        for i in range(3):
            row_frame = tk.Frame(grid_frame, bg="white")
            row_frame.pack()
            row_entries = []
            for j in range(3):
                entry = tk.Entry(row_frame, width=4, justify="center", 
                               font=("Arial", 16, "bold"), bd=2, relief="solid",
                               highlightbackground="#4CAF50", highlightthickness=1)
                entry.pack(side="left", padx=3, pady=3)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # Set default solvable puzzle
        default = [[1, 4, 2], [0, 3, 5], [6, 7, 8]]
        for i in range(3):
            for j in range(3):
                self.entries[i][j].insert(0, str(default[i][j]))
        
        # Algorithm selection
        ttk.Label(content, text="Select Algorithm", style="Subtitle.TLabel").pack(anchor="w", pady=(10, 10))
        
        self.algorithm = tk.StringVar(value="bfs")
        algorithms = [
            ("BFS", "bfs", "Breadth-First Search"),
            ("DFS", "dfs", "Depth-First Search"),
            ("IDDFS", "iddfs", "Iterative Deepening DFS"),
            ("A* (Manhattan)", "astar_manhattan", "A* with Manhattan Distance"),
            ("A* (Euclidean)", "astar_euclidean", "A* with Euclidean Distance")
        ]
        
        self.algo_buttons = []
        for short_text, value, tooltip in algorithms:
            btn_frame = tk.Frame(content, bg="white", cursor="hand2")
            btn_frame.pack(fill="x", pady=3)
            
            # Create custom radio button
            radio_canvas = tk.Canvas(btn_frame, width=20, height=20, bg="white", 
                                    highlightthickness=0)
            radio_canvas.pack(side="left", padx=(0, 8))
            
            label = tk.Label(btn_frame, text=short_text, font=("Arial", 11), 
                           bg="white", fg="#333", anchor="w")
            label.pack(side="left", fill="x", expand=True)
            
            # Bind click events
            for widget in [btn_frame, radio_canvas, label]:
                widget.bind("<Button-1>", lambda e, v=value: self.select_algorithm(v))
                # widget.bind("<Enter>", lambda e, f=btn_frame: f.configure(bg="#f5f5f5"))
                # widget.bind("<Leave>", lambda e, f=btn_frame: f.configure(bg="white"))
            
            self.algo_buttons.append((btn_frame, radio_canvas, value))
        
        self.update_algorithm_selection()
        
        # Solve button
        solve_btn = tk.Button(content, text="Solve Puzzle", 
                            font=("Arial", 12, "bold"),
                            bg="#4CAF50", fg="white", 
                            activebackground="#45a049",
                            activeforeground="white",
                            bd=0, pady=12, cursor="hand2",
                            command=self.solve_puzzle)
        solve_btn.pack(fill="x", pady=(15, 0))
        
        # Add hover effect
        solve_btn.bind("<Enter>", lambda e: solve_btn.configure(bg="#45a049"))
        solve_btn.bind("<Leave>", lambda e: solve_btn.configure(bg="#4CAF50"))
    
    def select_algorithm(self, value):
        self.algorithm.set(value)
        self.update_algorithm_selection()
    
    def update_algorithm_selection(self):
        selected = self.algorithm.get()
        for btn_frame, canvas, value in self.algo_buttons:
            canvas.delete("all")
            if value == selected:
                # Draw filled circle with checkmark
                canvas.create_oval(2, 2, 18, 18, fill="#4CAF50", outline="#2E7D32", width=2)
                canvas.create_line(6, 10, 9, 13, width=2, fill="white")
                canvas.create_line(9, 13, 14, 7, width=2, fill="white")
                btn_frame.configure(bg="white")
            else:
                # Draw empty circle
                canvas.create_oval(2, 2, 18, 18, fill="white", outline="#999", width=2)
                btn_frame.configure(bg="white")
    
    def create_info_frame(self, parent):
        info_container = tk.Frame(parent, bg="white", highlightbackground="#ddd", 
                                 highlightthickness=1)
        info_container.pack(fill="both", expand=True)
        
        # Title
        title = tk.Label(info_container, text="📊 Solution Info", 
                        font=("Arial", 16, "bold"), bg="white", fg="#333", pady=15)
        title.pack()
        
        # Info text
        self.info_text = tk.Text(info_container, height=6, wrap="word", 
                                font=("Arial", 11), bg="white", fg="#333",
                                bd=0, padx=20, pady=10)
        self.info_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.info_text.config(state="disabled")
        
        # Initial message
        self.info_text.config(state="normal")
        self.info_text.insert(1.0, "Enter an initial board state and select an algorithm to solve the puzzle.\n\nClick 'Solve Puzzle' to begin.")
        self.info_text.config(state="disabled")
    
    def draw_board(self, board):
        self.canvas.delete("all")
        cell_size = 120
        margin = 20
        corner_radius = 10
        
        for i in range(3):
            for j in range(3):
                x1 = margin + j * cell_size
                y1 = margin + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Draw rounded rectangle
                if board[i][j] == 0:
                    # Blank cell
                    self.draw_rounded_rect(self.canvas, x1+2, y1+2, x2-2, y2-2, 
                                          corner_radius, fill="#e0e0e0", outline="#bbb", width=2)
                else:
                    # Numbered cell with gradient effect
                    self.draw_rounded_rect(self.canvas, x1+2, y1+2, x2-2, y2-2, 
                                          corner_radius, fill="#4CAF50", outline="#2E7D32", width=3)
                    
                    # Add subtle shadow effect
                    self.canvas.create_text((x1 + x2) / 2 + 2, (y1 + y2) / 2 + 2, 
                                          text=str(board[i][j]), 
                                          font=("Arial", 40, "bold"), 
                                          fill="#2E7D32")
                    
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, 
                                          text=str(board[i][j]), 
                                          font=("Arial", 40, "bold"), 
                                          fill="white")
    
    def draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
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
        
        algo_names = {
            "bfs": "Breadth-First Search",
            "dfs": "Depth-First Search", 
            "iddfs": "Iterative Deepening DFS",
            "astar_manhattan": "A* (Manhattan Distance)",
            "astar_euclidean": "A* (Euclidean Distance)"
        }
        
        info = f"Algorithm: {algo_names.get(data['algorithm'], data['algorithm'])}\n\n"
        info += f"✓ Solution found!\n"
        info += f"• Cost: {data['cost']} moves\n"
        info += f"• Nodes Expanded: {data['nodes_expanded']:,}\n"
        info += f"• Search Depth: {data['search_depth']:,}\n"
        info += f"• Runtime: {data['runtime_ms']} ms"
        
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
            self.draw_arrow(self.left_arrow, "left", "disabled")
            self.draw_arrow(self.right_arrow, "right", "disabled")
            self.step_label.config(text="Step: 0 / 0")
            self.left_arrow.config(cursor="arrow")
            self.right_arrow.config(cursor="arrow")
            return
        
        self.step_label.config(text=f"Step: {self.current_step + 1} / {len(self.solution_path)}")
        
        if self.current_step <= 0:
            self.draw_arrow(self.left_arrow, "left", "disabled")
            self.left_arrow.config(cursor="arrow")
        else:
            self.draw_arrow(self.left_arrow, "left", "normal")
            self.left_arrow.config(cursor="hand2")
        
        if self.current_step >= len(self.solution_path) - 1:
            self.draw_arrow(self.right_arrow, "right", "disabled")
            self.right_arrow.config(cursor="arrow")
        else:
            self.draw_arrow(self.right_arrow, "right", "normal")
            self.right_arrow.config(cursor="hand2")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()