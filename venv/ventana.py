from tkinter import *
from tkinter import messagebox


# Una accion generica
def accion():
    print("Lo que hara")



# VentanaEmergente(Info)
def VEI():
    messagebox.showinfo("Hola", "holaaa como estas tu")
    import camara


# Declaracion de la ventana
ventana = Tk()

# Tamaño de la ventana
ventana.geometry("600x480")

# Titulo de la ventana
ventana.title("Titulo")

# Label
lbl = Label(ventana, text='El label')
lbl.pack(side=TOP)

# Button
btn = Button(ventana, text='El boton', command=VEI)
btn.pack(side=BOTTOM)


ventana.mainloop()