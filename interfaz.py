import customtkinter as ctk
current = [0]
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
sidebar = ctk.CTkFrame(master=app, width=150,border_width=2)
sidebar.pack(side="left", fill="y")

name = ctk.CTkFrame(sidebar,fg_color="red",height=100)
name.pack(side="top",fill="x",padx=2)
label_name = ctk.CTkLabel(name,text="Simplex Tableau")
label_name.pack(expand=True)

options = ctk.CTkFrame(sidebar,height=600,fg_color="transparent")
options.pack(side="bottom",pady=50,fill="x",padx=2)

buttons = []

for i in range(5):
    button = ctk.CTkButton(options, text=f"Tab {i + 1}", command=lambda i=i : change_frame(current[0],i),fg_color="transparent",corner_radius=0)
    button.pack(pady=10, fill="x",padx=2)
    buttons.append(button)
# Crear un contenedor para las pantallas
main = ctk.CTkFrame(master=app)
main.pack(side="right", fill="both", expand=True)


frames = []

for i in range(5):
    frame = ctk.CTkFrame(main) 
    frame.pack(fill="both", expand=True)
    label = ctk.CTkLabel(frame, text=f"This is the {i + 1} tab")
    label.pack(pady=10)
    frame.pack_forget()
    frames.append(frame)

frames[current[0]].pack(fill="both", expand=True)

app.mainloop()

