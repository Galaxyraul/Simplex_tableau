import customtkinter as ctk
import tableau_method as tm

current = ["Simplex Tableau"]
tableau = {}
tab_list = [
    "Simplex Tableau","Cargar archivo","Función Objetivo","Restricciones","Tableau"
]
tableau["objective"] = [0.5,0.5]
tableau["constraints"] = [[15000,5,2],[15000,2,5],[1000,1,0]]
tableau["operators"] = [1, 1,1]
tableau["coefficients"],tableau["base"],tableau["values"] = tm.build_tableau(tableau["objective"],tableau["constraints"],tableau["operators"])
operators_to_int = {">=":-1,"<=":1,"=":0}
tabs = {key:None for key in tab_list}


coefficients = []

buttons = []
def change_frame(remove,render):
    tabs[remove]["frame"].pack_forget()
    # Show the selected frame
    tabs[render]["frame"].pack(fill="both", expand=True)
    current[0] = render
    select_button(remove,render)

def select_button(remove,selected):
    tabs[remove]["button"].configure(fg_color="transparent")
    tabs[selected]["button"].configure(fg_color = "black")

def select_file(entry_path):
    # Abre un cuadro de diálogo para seleccionar un archivo
    file_path = ctk.filedialog.askopenfilename(title="Seleccionar archivo",
                                               filetypes=[("Archivos json", "*.json"), 
                                                          ("Todos los archivos", "*.*")])
    if file_path:
        entry_path.delete(0, "end")  # Borra lo que haya en el campo
        entry_path.insert(0, file_path)  # Inserta la ruta del archivo en el campo de entrada

def clear_frame(frame):
    for widget in frame.winfo_children():  # Itera sobre todos los hijos del frame
        widget.destroy()

def create_main_window():
    app = ctk.CTk()
    app.geometry("1200x800")
    app.title("Interfaz Principal")
    # Configuración del tema de CustomTkinter
    ctk.set_appearance_mode("dark")  # Cambiar a "light" si prefieres el modo claro
    ctk.set_default_color_theme("blue")  # Cambiar color del tema
    # Crear el frame izquierdo (menú lateral)

    main = ctk.CTkFrame(master=app)
    main.pack(side="right", fill="both", expand=True) 

    sidebar = ctk.CTkFrame(master=app, width=300,border_width=2)
    sidebar.pack(side="left", fill="y")

    name = ctk.CTkFrame(sidebar,fg_color="transparent",height=100)
    name.pack(side="top",fill="x",padx=2,pady = 20)

    options = ctk.CTkFrame(sidebar,height=600,fg_color="transparent")
    options.pack(side="bottom",pady=50,fill="x",padx=2)

    return app,main,name,options

def create_tabs(main,options,name):
    for i in tabs:
        frame = ctk.CTkFrame(main) 
        title = ctk.CTkFrame(frame,fg_color="transparent")
        title.pack(side="top",fill="x",pady=20)
        title = ctk.CTkLabel(title,font=("Arial",50),text=i)
        title.pack()
        content = ctk.CTkFrame(frame)
        content.pack(side="top",expand=True,fill="x")
        tabs[i]={"frame":frame,"content":content}
    for i in tabs:
        button = ctk.CTkButton(
                                name if i == "Simplex Tableau" else options, text=i,
                                command=lambda i=i : change_frame(current[0],i),
                                fg_color="transparent",corner_radius=0,
                                font=("Arial",18)
                                )
        button.pack(pady=10, fill="x")
        tabs[i]["button"]=button

def init_windows():
    welcome_window()
    load_from_file()
    f_objetivo()
    constraints_window()
    result_window()
    tabs[current[0]]["frame"].pack(fill="both", expand=True)
    tabs[current[0]]["button"].configure(fg_color="black",font=(("Arial",24)))

def welcome_window():
    label_intro = ctk.CTkLabel(tabs["Simplex Tableau"]["content"],wraplength=400,pady=20,font= ("Arial",18),anchor = "center",
                            text="Bienvenido a mi aplicación de simplex tableau para realizar un problema puedes cargarlo desde un archivo o introducirlo manualmente")
    load_btn = ctk.CTkButton(tabs["Simplex Tableau"]["content"],text="Cargar",command=lambda:change_frame(current[0],"Cargar archivo"))
    manual_btn = ctk.CTkButton(tabs["Simplex Tableau"]["content"],text="Manual",command=lambda:change_frame(current[0],"Función Objetivo"))

    label_intro.grid(row=0, column=0, columnspan=2, pady=20)  # La etiqueta ocupa ambas columnas
    load_btn.grid(row=1, column=0, padx=10, pady=10)
    manual_btn.grid(row=1, column=1, padx=10, pady=10)

    # Configurar las columnas para que se expandan
    tabs["Simplex Tableau"]["content"].grid_columnconfigure([0,1], weight=1)
    
def load_from_file():

    select_file_btn = ctk.CTkButton(tabs["Cargar archivo"]["content"], text="Seleccionar archivo", command= lambda:select_file(entry_path))
    entry_path = ctk.CTkEntry(tabs["Cargar archivo"]["content"], placeholder_text="Ruta del archivo", width=300)
    
    process_btn = ctk.CTkButton(tabs["Cargar archivo"]["content"],text="Ejecutar",command=lambda:tm.read_json(entry_path.get())) 
    select_file_btn.grid(row=2,column=0,sticky="e",pady=5,padx=2)
    process_btn.grid(row=3,column=0,pady=5,padx=2,columnspan=2)
    
    entry_path.grid(row=2,column=1,sticky="w",pady=5,padx=2)
    tabs["Cargar archivo"]["content"].grid_columnconfigure([0,1], weight=1)
    
def f_objetivo():
    header = ctk.CTkFrame(tabs["Función Objetivo"]["content"],fg_color="transparent")
    label_variables = ctk.CTkLabel(header,text="Número de variables:")
    n_variables = ctk.CTkEntry(header,placeholder_text="Introduce un valor")
    label_variables.grid(row=0,column=0,pady=10,padx=2)
    n_variables.grid(row=0,column=1,pady=10,padx=2)
    function = ctk.CTkFrame(tabs["Función Objetivo"]["content"],fg_color="transparent")
    accept_btn = ctk.CTkButton(header,text="Aceptar",command=lambda:show_obj(int(n_variables.get()),function,tabs["Función Objetivo"]["content"]))
    accept_btn.grid(row=0, column=2,padx=2)
    header.grid(row=0,column=0)
    function.grid(row=1,column = 0)
    tabs["Función Objetivo"]["content"].grid_columnconfigure([0],weight=1)
    #TODO Revisar cambiar número,arreglar display

def show_obj(n_variables,frame,frame2):
    clear_frame(frame)
    bottom = ctk.CTkFrame(frame2)
    fields = []
    label = ctk.CTkLabel(frame,text=f"Z=")
    label.grid(row=2,column=0,sticky="w")
    for i in range(n_variables):
        label = ctk.CTkLabel(frame,text=f"x{i+1}")
        label.grid(row=2,column=2*(i+1)-1,sticky="w",padx=2,pady=5)
        text_entry = ctk.CTkEntry(frame)
        text_entry.grid(row=2,column=2*(i+1),sticky="w",padx=2,pady=5)
        fields.append(text_entry)
    get_btn = ctk.CTkButton(bottom,text="Guardar",command=lambda:set_objective([float(entry.get()) for entry in fields]))
    bottom.grid(row=2,column=0)
    get_btn.pack()
    

def set_objective(values):
    tableau["objective"] = values
    change_frame(current[0],"Restricciones")
    
def add_constraint_row(frame,row,entries,operators):
    row[0] +=1
    row = row[0]
    fields = []
    last = 2 * len(tableau["objective"])
    label = ctk.CTkLabel(frame,text=f"R=")
    text_entry = ctk.CTkEntry(frame)
    fields.append(text_entry)
    entries.append(fields)
    label.grid(row=row,column=last + 1,pady=5,padx=2)
    text_entry.grid(row=row,column=last + 2,pady=5,padx=2)
    operator = ctk.CTkComboBox(frame,values=["=","<=",">="])
    operators.append(operator)
    operator.grid(row=row,column=last)
    for i in range(len(tableau["objective"])):
        label = ctk.CTkLabel(frame,text=f"x{i+1}=")
        label.grid(row=row,column=2*i,pady=5,padx=2)
        text_entry = ctk.CTkEntry(frame)
        text_entry.grid(row=row,column=2*i + 1,pady=5,padx=2)
        fields.append(text_entry)
        
def constraints_window():
    row = [0]
    entries = []
    operators = []
    header = ctk.CTkFrame(tabs["Restricciones"]["content"])
    constraints = ctk.CTkFrame(tabs["Restricciones"]["content"],fg_color="transparent")
    add_constraint_btn = ctk.CTkButton(header,text="Añadir restricción",command= lambda :add_constraint_row(constraints,row,entries,operators))
    get_values = ctk.CTkButton(header,text="Guardar restricciones",command=lambda:save_constraints(entries,operators))
    add_constraint_btn.grid(row = 0,column = 0,pady=5,padx=2)
    get_values.grid(row = 0,column = 1,pady=5,padx=2)
    header.grid(row=0)
    constraints.grid(row=1)
    tabs["Restricciones"]["content"].grid_columnconfigure([0],weight=1)

def save_constraints(entries,operators):
    tableau["constraints"] = [[float(entry.get()) for entry in constraint] for constraint in entries]
    tableau["operators"] = [operators_to_int[operator.get()] for operator in operators]
    print(tableau["objective"],tableau["constraints"],tableau["operators"])
    tableau["coefficients"],tableau["base"],tableau["values"] = tm.build_tableau(tableau["objective"],tableau["constraints"],tableau["operators"])
    clear_frame(tabs["Tableau"]["content"])
    result_window()
    change_frame(current[0],"Tableau")
    
def result_window():
    frame = tabs["Tableau"]["content"]
    to_solve = ctk.CTkFrame(frame,border_width=2,border_color="grey")
    print_table(to_solve,"coefficients","base","values")
    to_solve.grid(row=0,column=0,padx=5,pady=5)
    label = ctk.CTkLabel(to_solve,text=f"Original",font=("Arial",20))
    label.grid(row=0,column=1,padx=5,pady=5)
    solved = ctk.CTkFrame(frame,border_width=1,border_color="grey")
    label = ctk.CTkLabel(solved,text=f"Resuelto",font=("Arial",20))
    label.grid(row=0,column=1,padx=5,pady=5)
    frame.grid_columnconfigure([0,1], weight=1)
    resolve_btn = ctk.CTkButton(frame,text="Resolver",command=lambda:solve_tableau(solved,frame))        
    resolve_btn.grid(row=2,columnspan=2)

def solve_tableau(frame,frame2):
    tableau["base"],tableau["values"],tableau["result"]=tm.core(tableau["coefficients"],tableau["base"],tableau["values"])
    print(tableau["result"])
    print_table(frame,"coefficients","base","values")
    frame.grid(row=0,column=1,padx=5,pady=5)
    texto = f"Z={tableau["result"][0]} "

    for i in range(len(tableau["base"])):
        print(tableau["base"][i])
        if tableau["base"][i] < len(tableau["objective"]):
            texto += f"x{tableau["base"][i]}={tableau["values"][i,0]} "
    
    result_label = ctk.CTkLabel(frame2,text=texto,font=("Arial",20))
    result_label.grid(row=1,column=0,columnspan=2)
    print(tableau["result"])
 
    
def print_table(frame,key1,key2,key3):
    label = ctk.CTkLabel(frame,text=f"V.B",font=("Arial",20))
    label.grid(row=1,column=1,padx=5,pady=5)
    label = ctk.CTkLabel(frame,text=f"B",font=("Arial",20))
    label.grid(row=1,column=2,padx=5,pady=5)
    label = ctk.CTkLabel(frame,text=f"|C_i",font=("Arial",20))
    label.grid(row=0,column=2)
    for i in range(tableau[key1].shape[0]-1):
        label = ctk.CTkLabel(frame,text=f"|{tableau[key1][i + 1]}",font=("Arial",20))
        label.grid(row=1,column=i+3,padx=5)
        label = ctk.CTkLabel(frame,text=f"|x_{i+1}",font=("Arial",20))
        label.grid(row=0,column=i+3,padx=5,pady=5)
    for i in range(len(tableau[key2])):
        label = ctk.CTkLabel(frame,text=f"|x_{tableau[key2][i]}",font=("Arial",20))
        label.grid(row=i+2,column=1,padx=5,pady=5)
    for i in range(tableau[key3].shape[0]):
        for j in range(tableau[key3].shape[1]):
            label = ctk.CTkLabel(frame,text=f"|{tableau[key3][i,j]}",font=("Arial",20))
            label.grid(row=i+2,column=j+2,padx=5,pady=5)  
            
            
def main():
    app,main,name,options = create_main_window()
    create_tabs(main,options,name)
    init_windows()
    app.mainloop()
main()
