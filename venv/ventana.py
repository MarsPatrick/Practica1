from tkinter import Tk, Label, Button, messagebox

#Una accion generica
def accion():
    print("Lo que hara")

#VentanaEmergente(Info)
def VEI():
    messagebox.showinfo("Hola","hola como estas tu")


#Declaracion de la ventana
ventana = Tk()

#Tamaño de la ventana
ventana.geometry("600x480")

#Titulo de la ventana
ventana.title("Titulo")

#Label
lbl = Label(ventana, text='El label')
lbl.pack()

#Button
btn = Button(ventana, text='El boton', command=VEI)
btn.pack()

ventana.mainloop()