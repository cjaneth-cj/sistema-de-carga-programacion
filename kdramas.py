import tkinter as tk
from tkinter import messagebox, ttk
import gestion_kdramas as gk

COLOR_FONDO = "black"
COLOR_PRIMARIO = "darkOrchid4"
COLOR_TEXTO = "white"
COLOR_CAMPO = "#1a1a1a"
COLOR_TEXTO_CAMPO = "white"

class AppKDramas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Series Coreanas (K-Dramas)")
        self.root.geometry("880x640")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        gk.inicializar_sistema()

        self.modo_vista = "activos"
        self.crear_interfaz()
        self.actualizar_tabla()

    def crear_interfaz(self):
        lbl_titulo = tk.Label(
            self.root,
            text="🎬 GESTIÓN DE K-DRAMAS & PLATAFORMAS 🎬",
            font=("Helvetica", 17, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_TEXTO,
            pady=10,
        )
        lbl_titulo.pack(fill=tk.X)

        frame_superior = tk.Frame(self.root, bg=COLOR_FONDO, pady=10)
        frame_superior.pack(fill=tk.X, padx=20)

        frame_form = tk.LabelFrame(
            frame_superior,
            text=" Registrar / Editar K-Drama ",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            bd=2,
            relief=tk.GROOVE,
            padx=15,
            pady=10,
        )
        frame_form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        fields = [
            ("Código ID:", "entry_codigo"),
            ("Título:", "entry_titulo"),
            ("Género:", "entry_genero"),
            ("Plataforma:", "entry_plataforma"),
            ("Episodios:", "entry_episodios"),
        ]

        for i, (label_text, var_name) in enumerate(fields):
            lbl = tk.Label(
                frame_form,
                text=label_text,
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                anchor="w",
                font=("Helvetica", 10),
            )
            lbl.grid(row=i, column=0, sticky="w", pady=4)

            entry = tk.Entry(
                frame_form,
                bg=COLOR_CAMPO,
                fg=COLOR_TEXTO_CAMPO,
                insertbackground=COLOR_TEXTO,
                highlightbackground=COLOR_PRIMARIO,
                highlightcolor=COLOR_PRIMARIO,
                highlightthickness=1,
                font=("Helvetica", 10),
            )
            entry.grid(row=i, column=1, sticky="ew", pady=4, padx=(5, 0))
            setattr(self, var_name, entry)

        frame_form.columnconfigure(1, weight=1)

        frame_botones = tk.Frame(frame_superior, bg=COLOR_FONDO)
        frame_botones.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        btn_specs = [
            ("➕ Agregar Serie", COLOR_PRIMARIO, self.btn_agregar),
            ("🔍 Buscar (Código/Título)", "black", self.btn_buscar),
            ("📋 Ver Disponibles (Activos)", COLOR_PRIMARIO, self.ver_activos),
            ("🗑 Ver Retirados (Eliminados)", "black", self.ver_eliminados),
            ("⚠ Baja (Retirar)", COLOR_PRIMARIO, self.btn_baja),
            ("🔄 Reactivar Serie", "black", self.btn_reactivar),
        ]

        for texto, color_bg, comando in btn_specs:
            btn = tk.Button(
                frame_botones,
                text=texto,
                bg=color_bg,
                fg=COLOR_TEXTO,
                activebackground="white",
                activeforeground="black",
                font=("Helvetica", 9, "bold"),
                bd=1,
                relief=tk.RAISED,
                cursor="hand2",
                command=comando,
                width=24,
                pady=3,
            )
            btn.pack(pady=3)

        self.frame_tabla_header = tk.LabelFrame(
            self.root,
            text=" Series Disponibles en Plataformas ",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10,
        )
        self.frame_tabla_header.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="black",
            foreground="white",
            fieldbackground="black",
            rowheight=25,
            font=("Helvetica", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_PRIMARIO,
            foreground="white",
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", COLOR_PRIMARIO)],
            foreground=[("selected", "white")],
        )

        columnas = ("codigo", "titulo", "genero", "plataforma", "episodios")
        self.tabla = ttk.Treeview(
            self.frame_tabla_header,
            columns=columnas,
            show="headings",
            style="Treeview",
        )
        self.tabla.heading("codigo", text="Código ID")
        self.tabla.heading("titulo", text="Título de Serie")
        self.tabla.heading("genero", text="Género")
        self.tabla.heading("plataforma", text="Plataforma")
        self.tabla.heading("episodios", text="Episodios")

        self.tabla.column("codigo", width=90, anchor="center")
        self.tabla.column("titulo", width=260, anchor="w")
        self.tabla.column("genero", width=150, anchor="w")
        self.tabla.column("plataforma", width=140, anchor="center")
        self.tabla.column("episodios", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.frame_tabla_header,
            orient=tk.VERTICAL,
            command=self.tabla.yview,
        )
        self.tabla.configure(yscroll=scrollbar.set)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def limpiar_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_titulo.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.entry_plataforma.delete(0, tk.END)
        self.entry_episodios.delete(0, tk.END)

    def btn_agregar(self):
        codigo = self.entry_codigo.get()
        titulo = self.entry_titulo.get()
        genero = self.entry_genero.get()
        plataforma = self.entry_plataforma.get()
        episodios_str = self.entry_episodios.get()

        if not (
            codigo.strip()
            and titulo.strip()
            and genero.strip()
            and plataforma.strip()
            and episodios_str.strip()
        ):
            messagebox.showwarning("Campos Requeridos", "Por favor, llene todos los campos.")
            return

        try:
            episodios = int(episodios_str.strip())
            if episodios <= 0:
                messagebox.showerror("Error", "La cantidad de episodios debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error de Formato", "El campo 'Episodios' debe ser un número entero válido.")
            return

        exito, msg = gk.agregar_kdrama(codigo, titulo, genero, plataforma, episodios)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.ver_activos()
        else:
            messagebox.showerror("Error", msg)

    def btn_buscar(self):
        criterio = self.entry_codigo.get().strip() or self.entry_titulo.get().strip()
        if not criterio:
            messagebox.showwarning("Búsqueda", "Ingrese un Código o Título en el formulario para buscar.")
            return

        serie = gk.buscar_kdrama_activo(criterio)
        if serie:
            self.limpiar_campos()
            self.entry_codigo.insert(0, serie["codigo"])
            self.entry_titulo.insert(0, serie["titulo"])
            self.entry_genero.insert(0, serie["genero"])
            self.entry_plataforma.insert(0, serie["plataforma"])
            self.entry_episodios.insert(0, str(serie["episodios"]))
            messagebox.showinfo(
                "Encontrado",
                f"Serie Encontrada:\n- Título: {serie['titulo']}\n- Plataforma: {serie['plataforma']}",
            )
        else:
            messagebox.showinfo(
                "Sin Coincidencias",
                f"No se encontró ninguna serie activa que coincida con '{criterio}'.",
            )
#
    def btn_baja(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Código Requerido", "Ingrese el Código (ID) de la serie a dar de baja.")
            return

        serie = gk.buscar_kdrama_activo(codigo)
        if not serie:
            messagebox.showerror("No Encontrado", f"No existe serie activa con código '{codigo}'.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Baja Lógica",
            f"¿Desea dar de baja (retirar de plataforma) la serie '{serie['titulo']}'?",
        )
        if confirmar:
            exito, msg = gk.baja_logica(codigo)
            if exito:
                messagebox.showinfo("Baja Completada", msg)
                self.limpiar_campos()
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", msg)

    def btn_reactivar(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Código Requerido", "Ingrese el Código (ID) de la serie que desea reactivar.")
            return

        exito, msg = gk.reactivar_kdrama(codigo)
        if exito:
            messagebox.showinfo("Reactivación Completada", msg)
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", msg)

    def ver_activos(self):
        self.modo_vista = "activos"
        self.frame_tabla_header.config(text=" Series Disponibles en Plataformas ")
        self.actualizar_tabla()

    def ver_eliminados(self):
        self.modo_vista = "eliminados"
        self.frame_tabla_header.config(text=" Series Retiradas de Plataformas (Baja Lógica) ")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        lista = gk.datos_activos if self.modo_vista == "activos" else gk.datos_eliminados

        for serie in lista:
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    serie["codigo"],
                    serie["titulo"],
                    serie["genero"],
                    serie["plataforma"],
                    serie["episodios"],
                ),
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = AppKDramas(root)
    root.mainloop()