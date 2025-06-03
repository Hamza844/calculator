import tkinter as tk
from tkinter import font as tkfont, messagebox
from math import *
import json
import os

class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Advanced Scientific Calculator")
        self.geometry("500x750")
        self.resizable(False, False)
        self.theme = "dark"  # default theme
        self.history = []
        self.load_history()
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.display_font = tkfont.Font(family="Helvetica", size=24)
        self.button_font = tkfont.Font(family="Helvetica", size=16)
        self.history_font = tkfont.Font(family="Helvetica", size=10)
        
        # Colors for different themes
        self.themes = {
            "dark": {
                "bg": "#2E2E2E",
                "display_bg": "#1C1C1C",
                "display_fg": "white",
                "button_bg": "#505050",
                "button_fg": "white",
                "op_button_bg": "#FF9500",
                "sci_button_bg": "#3A3A3A",
                "history_bg": "#1C1C1C",
                "history_fg": "#AAAAAA"
            },
            "light": {
                "bg": "#F5F5F5",
                "display_bg": "#FFFFFF",
                "display_fg": "black",
                "button_bg": "#E0E0E0",
                "button_fg": "black",
                "op_button_bg": "#FF9500",
                "sci_button_bg": "#C0C0C0",
                "history_bg": "#FFFFFF",
                "history_fg": "#555555"
            },
            "blue": {
                "bg": "#1E3F66",
                "display_bg": "#0F2B4D",
                "display_fg": "white",
                "button_bg": "#3D5A80",
                "button_fg": "white",
                "op_button_bg": "#FF9500",
                "sci_button_bg": "#2D4B6E",
                "history_bg": "#0F2B4D",
                "history_fg": "#AAAAAA"
            }
        }
        
        # Variables
        self.current_input = tk.StringVar(value="0")
        self.total_expression = tk.StringVar(value="")
        self.memory = 0
        self.radians = True  # True for radians, False for degrees
        
        self.create_menu()
        self.create_display()
        self.create_buttons()
        self.create_history_panel()
        self.apply_theme()
        self.bind_keys()
        
    def create_menu(self):
        menubar = tk.Menu(self)
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Dark", command=lambda: self.set_theme("dark"))
        theme_menu.add_command(label="Light", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Blue", command=lambda: self.set_theme("blue"))
        menubar.add_cascade(label="Themes", menu=theme_menu)
        
        # Mode menu
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_command(label="Radians", command=lambda: self.set_radians(True))
        mode_menu.add_command(label="Degrees", command=lambda: self.set_radians(False))
        menubar.add_cascade(label="Mode", menu=mode_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Functions Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
    
    def create_display(self):
        # Frame for display
        display_frame = tk.Frame(self, bg=self.themes[self.theme]["display_bg"], padx=10, pady=10)
        display_frame.pack(fill="x")
        
        # Mode indicator
        self.mode_label = tk.Label(
            display_frame, 
            text="RAD" if self.radians else "DEG",
            font=self.button_font,
            bg=self.themes[self.theme]["display_bg"],
            fg=self.themes[self.theme]["display_fg"],
            anchor="w"
        )
        self.mode_label.pack(fill="x")
        
        # Memory label
        self.memory_label = tk.Label(
            display_frame, 
            text="",
            font=self.button_font,
            bg=self.themes[self.theme]["display_bg"],
            fg=self.themes[self.theme]["display_fg"],
            anchor="e"
        )
        self.memory_label.pack(fill="x")
        
        # Total expression label
        total_label = tk.Label(
            display_frame, 
            textvariable=self.total_expression, 
            font=self.button_font,
            bg=self.themes[self.theme]["display_bg"],
            fg=self.themes[self.theme]["display_fg"],
            anchor="e"
        )
        total_label.pack(fill="x")
        
        # Current input label
        input_label = tk.Label(
            display_frame, 
            textvariable=self.current_input, 
            font=self.display_font,
            bg=self.themes[self.theme]["display_bg"],
            fg=self.themes[self.theme]["display_fg"],
            anchor="e"
        )
        input_label.pack(fill="x")
    
    def create_buttons(self):
        # Main button frame
        button_frame = tk.Frame(self, bg=self.themes[self.theme]["bg"])
        button_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Scientific buttons (top row)
        sci_frame = tk.Frame(button_frame, bg=self.themes[self.theme]["bg"])
        sci_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        
        sci_buttons = [
            "sin", "cos", "tan", "log", "ln",
            "asin", "acos", "atan", "π", "e"
        ]
        
        for i, text in enumerate(sci_buttons):
            sci_frame.columnconfigure(i, weight=1)
            btn = tk.Button(
                sci_frame,
                text=text,
                font=self.button_font,
                bg=self.themes[self.theme]["sci_button_bg"],
                fg=self.themes[self.theme]["button_fg"],
                activebackground="#555555",
                activeforeground="white",
                relief="flat",
                borderwidth=0,
                command=lambda x=text: self.on_scientific_button(x)
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
        
        # Standard calculator buttons
        std_frame = tk.Frame(button_frame, bg=self.themes[self.theme]["bg"])
        std_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        
        button_layout = [
            ["MC", "MR", "M+", "M-", "⌫"],
            ["(", ")", "^", "/", "C"],
            ["7", "8", "9", "*", "√"],
            ["4", "5", "6", "-", "%"],
            ["1", "2", "3", "+", "="],
            ["0", ".", "±", "AC", "x²"]
        ]
        
        for i, row in enumerate(button_layout):
            std_frame.rowconfigure(i, weight=1)
            for j, button_text in enumerate(row):
                std_frame.columnconfigure(j, weight=1)
                
                # Special styling
                if button_text == "=":
                    bg_color = self.themes[self.theme]["op_button_bg"]
                elif button_text in ["⌫", "C", "AC"]:
                    bg_color = self.themes[self.theme]["button_bg"]
                elif button_text in ["MC", "MR", "M+", "M-"]:
                    bg_color = self.themes[self.theme]["sci_button_bg"]
                else:
                    bg_color = self.themes[self.theme]["button_bg"]
                
                button = tk.Button(
                    std_frame,
                    text=button_text,
                    font=self.button_font,
                    bg=bg_color,
                    fg=self.themes[self.theme]["button_fg"],
                    activebackground="#555555",
                    activeforeground="white",
                    relief="flat",
                    borderwidth=0,
                    command=lambda x=button_text: self.on_button_click(x)
                )
                button.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
    
    def create_history_panel(self):
        history_frame = tk.Frame(self, bg=self.themes[self.theme]["history_bg"])
        history_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(
            history_frame,
            text="History",
            font=self.title_font,
            bg=self.themes[self.theme]["history_bg"],
            fg=self.themes[self.theme]["history_fg"]
        ).pack(fill="x")
        
        self.history_text = tk.Text(
            history_frame,
            font=self.history_font,
            bg=self.themes[self.theme]["history_bg"],
            fg=self.themes[self.theme]["history_fg"],
            state="disabled",
            height=8,
            padx=5,
            pady=5,
            wrap="word"
        )
        self.history_text.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.history_text)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        # Populate with existing history
        self.update_history_display()
    
    def apply_theme(self):
        theme = self.themes[self.theme]
        self.configure(bg=theme["bg"])
        
        # Update display
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
        
        # Update all buttons (this is simplified - in a real app you'd track all buttons)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Button):
                        if widget["text"] == "=":
                            widget.config(bg=theme["op_button_bg"], fg=theme["button_fg"])
                        elif widget["text"] in ["⌫", "C", "AC"]:
                            widget.config(bg=theme["button_bg"], fg=theme["button_fg"])
                        elif widget["text"] in ["MC", "MR", "M+", "M-"]:
                            widget.config(bg=theme["sci_button_bg"], fg=theme["button_fg"])
                        else:
                            widget.config(bg=theme["button_bg"], fg=theme["button_fg"])
    
    def bind_keys(self):
        self.bind("<Return>", lambda event: self.evaluate())
        self.bind("<Escape>", lambda event: self.clear_all())
        self.bind("<BackSpace>", lambda event: self.backspace())
        
        # Number keys
        for num in "0123456789":
            self.bind(num, lambda event, x=num: self.add_to_input(x))
            
        # Operator keys
        self.bind("+", lambda event: self.add_to_input("+"))
        self.bind("-", lambda event: self.add_to_input("-"))
        self.bind("*", lambda event: self.add_to_input("*"))
        self.bind("/", lambda event: self.add_to_input("/"))
        self.bind("^", lambda event: self.add_to_input("^"))
        self.bind("%", lambda event: self.add_to_input("%"))
        self.bind(".", lambda event: self.add_to_input("."))
        self.bind("(", lambda event: self.add_to_input("("))
        self.bind(")", lambda event: self.add_to_input(")"))
        
        # Scientific functions
        self.bind("p", lambda event: self.add_to_input("pi"))
        self.bind("e", lambda event: self.add_to_input("e"))
    
    def set_theme(self, theme_name):
        self.theme = theme_name
        self.apply_theme()
    
    def set_radians(self, radians):
        self.radians = radians
        self.mode_label.config(text="RAD" if radians else "DEG")
    
    def update_memory_label(self):
        if self.memory != 0:
            self.memory_label.config(text=f"M: {self.memory}")
        else:
            self.memory_label.config(text="")
    
    def add_to_history(self, expression, result):
        entry = f"{expression} = {result}"
        self.history.append(entry)
        
        # Keep only the last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        self.update_history_display()
        self.save_history()
    
    def update_history_display(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        
        for item in reversed(self.history):
            self.history_text.insert("end", item + "\n")
        
        self.history_text.config(state="disabled")
        self.history_text.see("end")
    
    def save_history(self):
        try:
            with open("calculator_history.json", "w") as f:
                json.dump(self.history, f)
        except:
            pass
    
    def load_history(self):
        if os.path.exists("calculator_history.json"):
            try:
                with open("calculator_history.json", "r") as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def show_about(self):
        messagebox.showinfo(
            "About",
            "Advanced Scientific Calculator\n\n"
            "Features:\n"
            "- Basic and scientific operations\n"
            "- Memory functions\n"
            "- Calculation history\n"
            "- Multiple themes\n"
            "- Radians/Degrees mode\n\n"
            "Created with Python and Tkinter"
        )
    
    def show_help(self):
        messagebox.showinfo(
            "Functions Help",
            "Available functions:\n\n"
            "sin/cos/tan - Trigonometric functions\n"
            "asin/acos/atan - Inverse trigonometric\n"
            "log - Base 10 logarithm\n"
            "ln - Natural logarithm\n"
            "√ - Square root\n"
            "x² - Square\n"
            "^ - Power\n"
            "π - Pi constant (3.1415...)\n"
            "e - Euler's number (2.7182...)\n\n"
            "Use parentheses for complex expressions"
        )
    
    def on_button_click(self, button_text):
        if button_text.isdigit() or button_text == ".":
            self.add_to_input(button_text)
        elif button_text in ["+", "-", "*", "/", "^", "%", "(", ")"]:
            self.add_operator(button_text)
        elif button_text == "=":
            self.evaluate()
        elif button_text == "⌫":
            self.backspace()
        elif button_text == "C":
            self.clear()
        elif button_text == "AC":
            self.clear_all()
        elif button_text == "±":
            self.negate()
        elif button_text == "√":
            self.square_root()
        elif button_text == "x²":
            self.square()
        elif button_text == "MC":
            self.memory_clear()
        elif button_text == "MR":
            self.memory_recall()
        elif button_text == "M+":
            self.memory_add()
        elif button_text == "M-":
            self.memory_subtract()
    
    def on_scientific_button(self, button_text):
        try:
            current = self.current_input.get()
            
            if button_text == "π":
                self.current_input.set("pi")
            elif button_text == "e":
                self.current_input.set("e")
            elif button_text in ["sin", "cos", "tan", "asin", "acos", "atan"]:
                value = float(current)
                if not self.radians:
                    value = radians(value)
                
                if button_text == "sin":
                    result = sin(value)
                elif button_text == "cos":
                    result = cos(value)
                elif button_text == "tan":
                    result = tan(value)
                elif button_text == "asin":
                    result = asin(value)
                elif button_text == "acos":
                    result = acos(value)
                elif button_text == "atan":
                    result = atan(value)
                
                if not self.radians and button_text in ["asin", "acos", "atan"]:
                    result = degrees(result)
                
                self.current_input.set(str(result))
                self.total_expression.set(f"{button_text}({current})")
            elif button_text == "log":
                result = log10(float(current))
                self.current_input.set(str(result))
                self.total_expression.set(f"log({current})")
            elif button_text == "ln":
                result = log(float(current))
                self.current_input.set(str(result))
                self.total_expression.set(f"ln({current})")
        except:
            self.current_input.set("Error")
    
    def add_to_input(self, value):
        current = self.current_input.get()
        
        if current == "0" and value != ".":
            self.current_input.set(value)
        else:
            self.current_input.set(current + value)
    
    def add_operator(self, operator):
        current = self.current_input.get()
        self.total_expression.set(self.total_expression.get() + current + operator)
        self.current_input.set("0")
    
    def clear(self):
        self.current_input.set("0")
    
    def clear_all(self):
        self.current_input.set("0")
        self.total_expression.set("")
    
    def backspace(self):
        current = self.current_input.get()
        if len(current) == 1:
            self.current_input.set("0")
        else:
            self.current_input.set(current[:-1])
    
    def negate(self):
        current = self.current_input.get()
        if current.startswith("-"):
            self.current_input.set(current[1:])
        else:
            self.current_input.set("-" + current)
    
    def square_root(self):
        try:
            value = float(self.current_input.get())
            if value >= 0:
                result = sqrt(value)
                self.current_input.set(str(result))
                self.total_expression.set("√(" + str(value) + ")")
            else:
                self.current_input.set("Error")
        except:
            self.current_input.set("Error")
    
    def square(self):
        try:
            value = float(self.current_input.get())
            result = value ** 2
            self.current_input.set(str(result))
            self.total_expression.set("(" + str(value) + ")²")
        except:
            self.current_input.set("Error")
    
    def memory_clear(self):
        self.memory = 0
        self.update_memory_label()
    
    def memory_recall(self):
        self.current_input.set(str(self.memory))
    
    def memory_add(self):
        try:
            value = float(self.current_input.get())
            self.memory += value
            self.update_memory_label()
        except:
            pass
    
    def memory_subtract(self):
        try:
            value = float(self.current_input.get())
            self.memory -= value
            self.update_memory_label()
        except:
            pass
    
    def evaluate(self):
        try:
            expression = self.total_expression.get() + self.current_input.get()
            
            # Replace special constants and functions
            expression = expression.replace("^", "**")
            expression = expression.replace("π", "pi")
            expression = expression.replace("√", "sqrt")
            
            # Handle percentage
            if "%" in expression:
                parts = expression.split("%")
                if len(parts) == 2:
                    value = float(parts[0])
                    percent = float(parts[1])
                    result = value * percent / 100
                    self.current_input.set(str(result))
                    self.total_expression.set("")
                    self.add_to_history(f"{value}% of {percent}", result)
                    return
            
            result = eval(expression, {"__builtins__": None}, {
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "asin": asin,
                "acos": acos,
                "atan": atan,
                "log": log10,
                "ln": log,
                "sqrt": sqrt,
                "pi": pi,
                "e": e,
                "radians": radians,
                "degrees": degrees
            })
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Round to 10 decimal places to avoid floating point weirdness
                    result = round(result, 10)
            
            self.current_input.set(str(result))
            self.add_to_history(expression, result)
            self.total_expression.set("")
        except:
            self.current_input.set("Error")

if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()