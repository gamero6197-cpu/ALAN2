import tkinter as tk


class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("ALAN")
        self.root.resizable(False, False)

        self.pantalla = tk.StringVar(value="")

        tk.Label(
            root, text="ALAN", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white",
            padx=20, pady=10
        ).grid(row=0, column=0, columnspan=4, sticky="we")

        tk.Entry(
            root, textvariable=self.pantalla, font=("Arial", 18),
            justify="right", state="readonly", width=16, bd=5
        ).grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        botones = [
            ("C", 2, 0), ("←", 2, 1), ("%", 2, 2), ("/", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("*", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2, 2),
        ]

        for b in botones:
            texto, fila, col = b[0], b[1], b[2]
            colspan = b[3] if len(b) > 3 else 1
            color = "#e74c3c" if texto in ("C", "←") else "#3498db" if texto == "=" else "#ecf0f1"
            tk.Button(
                root, text=texto, font=("Arial", 14, "bold"), width=5, height=2,
                bg=color, activebackground="#bdc3c7",
                command=lambda t=texto: self.presionar(t)
            ).grid(row=fila, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")

    def presionar(self, texto):
        valor = self.pantalla.get()
        if texto == "C":
            self.pantalla.set("")
        elif texto == "←":
            self.pantalla.set(valor[:-1])
        elif texto == "=":
            try:
                resultado = eval(valor.replace("%", "/100"))
                self.pantalla.set(str(resultado))
            except Exception:
                self.pantalla.set("Error")
        else:
            self.pantalla.set(valor + texto)


if __name__ == "__main__":
    ventana = tk.Tk()
    Calculadora(ventana)
    ventana.mainloop()
