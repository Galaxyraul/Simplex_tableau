import customtkinter as ctk
current = [0]
tab_list = [
    "Simplex Tableau","Cargar archivo","Función Objetivo","Restricciones","Tableau","Historial"
]
def change_frame(remove,render):
    print(f"cambiando pestañas {remove,render}")
    frames[remove].pack_forget()
    # Show the selected frame
    frames[render].pack(fill="both", expand=True)
    current[0] = render
    select_button(remove,render)

def select_button(remove,selected):
    buttons[remove].configure(fg_color="transparent")
    buttons[selected].configure(fg_color = "blue")
# Configuración del tema de CustomTkinter
ctk.set_appearance_mode("dark")  # Cambiar a "light" si prefieres el modo claro
ctk.set_default_color_theme("blue")  # Cambiar color del tema

# Crear la ventana principal
app = ctk.CTk()
app.geometry("1000x800")
app.title("Interfaz Principal")

# Crear el frame izquierdo (menú lateral)
sidebar = ctk.CTkFrame(master=app, width=300,border_width=2)
sidebar.pack(side="left", fill="y")

name = ctk.CTkFrame(sidebar,fg_color="red",height=100)
name.pack(side="top",fill="x",padx=2,pady = 20)

options = ctk.CTkFrame(sidebar,height=600,fg_color="transparent")
options.pack(side="bottom",pady=50,fill="x",padx=2)

main = ctk.CTkFrame(master=app)
main.pack(side="right", fill="both", expand=True)

buttons = []
for i in range(len(tab_list)):
    button = ctk.CTkButton(
                            options if i != 0 else name, text=tab_list[i],
                            command=lambda i=i : change_frame(current[0],i),
                            fg_color="transparent",corner_radius=0,
                            font=("Arial",18)
                            )
    button.pack(pady=10, fill="x")
    buttons.append(button)
# Crear un contenedor para las pantallas

frames = []
contents = []
for i in range(len(tab_list)):
    frame = ctk.CTkFrame(main) 
    title = ctk.CTkFrame(frame,fg_color="blue")
    title.pack(side="top",fill="x")
    title = ctk.CTkLabel(title,font=("Arial",24),text=tab_list[i])
    title.pack()
    content = ctk.CTkFrame(frame,fg_color="red")
    content.pack(side="top",expand=True,fill="x")
    frames.append(frame)
    contents.append(content)

def welcome_window():
    label_intro = ctk.CTkLabel(contents[0],wraplength=300,pady=20,font= ("Arial",18),anchor = "center",
                           text="Bienvenido a mi aplicación de simplex tableau para realizar un problema puedes cargarlo desde un archivo o introducirlo manualmente")
    load_btn = ctk.CTkButton(contents[0],text="Cargar")
    manual_btn = ctk.CTkButton(contents[0],text="Manual")

    label_intro.grid(row=0, column=0, columnspan=2, pady=20)  # La etiqueta ocupa ambas columnas
    load_btn.grid(row=1, column=0, padx=10, pady=10)
    manual_btn.grid(row=1, column=1, padx=10, pady=10)

    # Configurar las columnas para que se expandan
    contents[0].grid_columnconfigure(0, weight=1)
    contents[0].grid_columnconfigure(1, weight=1)

def load_from_file():
    n_problems = ctk.CTkEntry(contents[1],placeholder_text="Introduce un valor")
    label_problems = ctk.CTkLabel(contents[1],text="número de problemas:")
    separator = ctk.CTkEntry(contents[1],placeholder_text="Introduce un valor")
    label_separator = ctk.CTkLabel(contents[1],text="separador:")
    
    label_problems.grid(row=0,column=0,pady=0)
    label_separator.grid(row=1,column=0,pady=0)
    
    n_problems.grid(row=0,column=1)
    separator.grid(row=1,column=1)
    

welcome_window()
load_from_file()
frames[current[0]].pack(fill="both", expand=True)
buttons[current[0]].configure(fg_color="blue",font=(("Arial",24)))
app.mainloop()

