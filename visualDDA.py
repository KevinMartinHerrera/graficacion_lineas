import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from calculate_line_direction import CalculateLineDirection
from calculate_slope import CalculateSlope
from dda_line_class import LineaDDA
import csv

class UltimateLineVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Line Visualizer Pro")
        self.root.geometry("1300x850")
        self.dark_mode = False
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.update_styles()
        
    def update_styles(self):
        base_bg = "#2d3436" if self.dark_mode else "#f5f6fa"
        text_color = "#ffffff" if self.dark_mode else "#2d3436"
        button_bg = "#0984e3" if self.dark_mode else "#74b9ff"
        
        self.style.configure("TFrame", background=base_bg)
        self.style.configure("TLabel", background=base_bg, foreground=text_color)
        self.style.configure("TButton", background=button_bg, foreground="white")
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"), foreground=text_color)
        self.style.configure("Data.TLabel", background=base_bg, foreground=text_color)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Sección de entrada
        input_frame = ttk.LabelFrame(left_frame, text="🔢 Coordenadas", padding=15)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Punto A (X1, Y1):", style="Header.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.x1_entry = ttk.Entry(input_frame, width=10)
        self.x1_entry.grid(row=0, column=1, padx=5)
        self.y1_entry = ttk.Entry(input_frame, width=10)
        self.y1_entry.grid(row=0, column=2, padx=5)

        ttk.Label(input_frame, text="Punto B (X2, Y2):", style="Header.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.x2_entry = ttk.Entry(input_frame, width=10)
        self.x2_entry.grid(row=1, column=1, padx=5)
        self.y2_entry = ttk.Entry(input_frame, width=10)
        self.y2_entry.grid(row=1, column=2, padx=5)

        # Botones
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="🖌️ Generar", command=self.draw_line).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🧹 Limpiar", command=self.clear_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="💾 CSV", command=self.export_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🌓 Tema", command=self.toggle_theme).pack(side=tk.LEFT, padx=2)

        # Información
        data_frame = ttk.LabelFrame(left_frame, text="📊 Datos", padding=15)
        data_frame.pack(fill=tk.BOTH, pady=10)

        self.direction_label = ttk.Label(data_frame, style="Data.TLabel")
        self.direction_label.pack(fill=tk.X, pady=3)
        self.slope_label = ttk.Label(data_frame, style="Data.TLabel")
        self.slope_label.pack(fill=tk.X, pady=3)
        self.points_label = ttk.Label(data_frame, style="Data.TLabel")
        self.points_label.pack(fill=tk.X, pady=3)

        # Tabla
        table_frame = ttk.LabelFrame(left_frame, text="📑 Puntos Generados", padding=15)
        table_frame.pack(fill=tk.BOTH, expand=True)
        self.table = ttk.Treeview(table_frame, columns=("X", "Y"), show="headings", height=12)
        self.table.heading("X", text="X")
        self.table.heading("Y", text="Y")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Gráfica
        fig = plt.figure(figsize=(8, 6), facecolor="#2d3436" if self.dark_mode else "#f5f6fa")
        self.ax = fig.add_subplot(111)
        self.setup_plot_style()
        
        self.canvas = FigureCanvasTkAgg(fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)
        self.toolbar = NavigationToolbar2Tk(self.canvas, main_frame)
        self.toolbar.update()

    def setup_plot_style(self):
        bg_color = "#2d3436" if self.dark_mode else "#ffffff"
        text_color = "#ffffff" if self.dark_mode else "#000000"
        grid_color = "#636e72" if self.dark_mode else "#dcdde1"

        self.ax.set_facecolor(bg_color)
        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, 500)
        self.ax.tick_params(colors=text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.title.set_color(text_color)
        self.ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_styles()
        self.setup_plot_style()
        self.canvas.draw()

    def clear_all(self):
        self.x1_entry.delete(0, tk.END)
        self.y1_entry.delete(0, tk.END)
        self.x2_entry.delete(0, tk.END)
        self.y2_entry.delete(0, tk.END)
        self.ax.clear()
        self.setup_plot_style()
        self.canvas.draw()
        self.table.delete(*self.table.get_children())
        self.direction_label.config(text="")
        self.slope_label.config(text="")
        self.points_label.config(text="")

    def draw_line(self):
        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())
            
            if not (0 <= x1 <= 500 and 0 <= y1 <= 500 and 0 <= x2 <= 500 and 0 <= y2 <= 500):
                raise ValueError("Rango permitido: 0-500")
            if (x1, y1) == (x2, y2):
                raise ValueError("Los puntos deben ser diferentes")

            A, B = (x1, y1), (x2, y2)
            direction = CalculateLineDirection(A, B).line_direction()
            slope = CalculateSlope(A, B).slope()
            line = LineaDDA(A, B, slope, direction)
            points = line.calculate_line()

            self.ax.clear()
            self.setup_plot_style()
            line_color = "#ff7675" if self.dark_mode else "#d63031"
            self.ax.plot([x1, x2], [y1, y2], color=line_color, linewidth=3)
            self.ax.plot(x1, y1, 'o', markersize=10, color="#74b9ff")
            self.ax.plot(x2, y2, 'o', markersize=10, color="#55efc4")
            self.ax.set_title(f"Línea: ({x1}, {y1}) → ({x2}, {y2})", fontsize=12)
            self.canvas.draw()

            direction_desc = {
                1: "↗ Izquierda-Derecha | Abajo-Arriba",
                2: "↘ Izquierda-Derecha | Arriba-Abajo",
                3: "→ Horizontal Derecha",
                4: "↖ Derecha-Izquierda | Abajo-Arriba",
                5: "↙ Derecha-Izquierda | Arriba-Abajo",
                6: "← Horizontal Izquierda",
                7: "↑ Vertical Arriba",
                8: "↓ Vertical Abajo"
            }
            
            self.direction_label.config(text=f"Dirección: {direction_desc[direction]} (Caso {direction})")
            self.slope_label.config(text=f"Pendiente: {slope if slope is not None else 'Infinita'}")
            self.points_label.config(text=f"Puntos Generados: {len(points)}")
            
            self.table.delete(*self.table.get_children())
            for p in points:
                self.table.insert("", "end", values=(round(p[0], 2), round(p[1], 2)))

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

    def export_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if not file_path: return
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])
                for child in self.table.get_children():
                    writer.writerow(self.table.item(child)['values'])
            
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateLineVisualizer(root)
    root.mainloop()