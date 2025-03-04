import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from core.calculate_line_direction.calculate_line_direction import CalculateLineDirection
from core.calculate_slope.calculate_slope import CalculateSlope
from core.dda_line.dda_line import DDALinea
import csv
from models.triangle_model import TriangleModel
from core.calculate_triangle.triangle import Triangle

class UltimateLineVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Line Visualizer Pro")
        self.root.geometry("1300x850")
        self.dark_mode = False
        self.triangle_mode = False
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

        # Campos para triángulo (ocultos inicialmente)
        self.x3_label = ttk.Label(input_frame, text="Punto C (X3, Y3):", style="Header.TLabel")
        self.x3_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.x3_entry = ttk.Entry(input_frame, width=10)
        self.x3_entry.grid(row=2, column=1, padx=5)
        self.y3_entry = ttk.Entry(input_frame, width=10)
        self.y3_entry.grid(row=2, column=2, padx=5)
        self.x3_label.grid_remove()
        self.x3_entry.grid_remove()
        self.y3_entry.grid_remove()

        # Botones
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="🖌️ Generar", command=self.draw_geometry).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔺 Triángulo", command=self.toggle_triangle_mode).pack(side=tk.LEFT, padx=2)
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

    def toggle_triangle_mode(self):
        self.triangle_mode = not self.triangle_mode
        if self.triangle_mode:
            self.x3_label.grid()
            self.x3_entry.grid()
            self.y3_entry.grid()
        else:
            self.x3_label.grid_remove()
            self.x3_entry.grid_remove()
            self.y3_entry.grid_remove()
        self.clear_all()

    def clear_all(self):
        for entry in [self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry, self.x3_entry, self.y3_entry]:
            entry.delete(0, tk.END)
        self.ax.clear()
        self.setup_plot_style()
        self.canvas.draw()
        self.table.delete(*self.table.get_children())
        self.direction_label.config(text="")
        self.slope_label.config(text="")
        self.points_label.config(text="")

    def draw_geometry(self):
        if self.triangle_mode:
            self.draw_triangle()
        else:
            self.draw_line()

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
            line = DDALinea(A, B, slope, direction)
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

    def draw_triangle(self):
        try:
            A = (float(self.x1_entry.get()), float(self.y1_entry.get()))
            B = (float(self.x2_entry.get()), float(self.y2_entry.get()))
            C = (float(self.x3_entry.get()), float(self.y3_entry.get()))
            
            # Validar colinealidad
            area = abs((B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]) + A[0]*(B[1]-C[1]))) / 2
            if area < 1:
                raise ValueError("¡Los puntos deben formar un triángulo válido!")
            
            triangle_model = TriangleModel(A, B, C)
            triangle = Triangle(triangle_model)
            filled_data = triangle.calculate_triangle_fill()

            self.ax.clear()
            self.setup_plot_style()
            line_color = "#ff7675" if self.dark_mode else "#d63031"
            fill_color = "#ff767540" if self.dark_mode else "#74b9ff40"

            # Dibujar bordes
            self.ax.plot([A[0], B[0]], [A[1], B[1]], color=line_color, linewidth=3)
            self.ax.plot([B[0], C[0]], [B[1], C[1]], color=line_color, linewidth=3)
            self.ax.plot([C[0], A[0]], [C[1], A[1]], color=line_color, linewidth=3)

            # Relleno optimizado
            segments = []
            for fill_line in filled_data["AC"]:
                points = fill_line["coordenadas"]
                if len(points) >= 2:
                    segments.append([(points[0][0], points[0][1]), (points[-1][0], points[-1][1])])
            
            lc = LineCollection(segments, colors=fill_color, linewidths=1)
            self.ax.add_collection(lc)
            
            self._update_triangle_ui(filled_data, area)
            self.canvas.draw()

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error en triángulo:\n{str(e)}")

    def _update_triangle_ui(self, filled_data, area):
        all_points = set()
        
        # Procesar bordes
        for edge in [filled_data["AB"], filled_data["BC"]]:
            for p in edge["coordenadas"]:
                all_points.add((round(p[0], 2), round(p[1], 2)))
        
        # Procesar relleno
        for fill_line in filled_data["AC"]:
            for p in fill_line["coordenadas"]:
                all_points.add((round(p[0], 2), round(p[1], 2)))

        # Actualizar tabla
        self.table.delete(*self.table.get_children())
        for p in sorted(all_points, key=lambda x: (x[0], x[1])):
            self.table.insert("", "end", values=p)

        # Actualizar labels
        self.direction_label.config(text="Triángulo Rellenado")
        self.slope_label.config(text=f"Área: {area:.2f} px²")
        self.points_label.config(text=f"Total Puntos: {len(all_points)}")

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