from tkinter import *

# Una accion generica
def accion():
    print("Lo que hara")


# VentanaEmergente(Info)
def VEI():
    messagebox.showinfo("Hola", "holaaa como estas tu")


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

jajajameequivoque

ventana.mainloop()