import ttkbootstrap as ttk


def main():
    root = ttk.Window(themename="darkly")
    ttk.Label(root, text="Привет!").pack(padx=40, pady=20)
    root.mainloop()


