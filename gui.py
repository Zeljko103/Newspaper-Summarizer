import tkinter as tk
from tkinter import messagebox
from typing import Optional, List

from moj_clanak import MojClanak


class GUI:
    def __init__(self):

        self.glavni_prozor: tk = tk.Tk()
        self.glavni_prozor.title("Sažete vijesti")
        self.glavni_prozor.geometry('1230x800')

        self.__clanak: MojClanak = MojClanak()
        self.__lista_clanaka: Optional[List[str]] = None

        self.__naslov: Optional[tk.Text] = None
        self.__autor: Optional[tk.Text] = None
        self.__datum: Optional[tk.Text] = None
        self.__rezime: Optional[tk.Text] = None
        self.__osjecanje: Optional[tk.Text] = None
        self.__url: Optional[tk.Text] = None
        self.__filtriranje: Optional[tk.Text] = None

        self.__filtriranje_ukljuci: tk.BooleanVar = tk.BooleanVar()
        self.__da_ne: tk.BooleanVar = tk.BooleanVar()
        self.__filtriranje_zavrseno: tk.BooleanVar = tk.BooleanVar()
        self.__trenutni: tk.IntVar = tk.IntVar()
        self.__prethodni: Optional[tk.Button] = None
        self.__sledeci: Optional[tk.Button] = None

    def popuni_glavni_prozor(self) -> None:
        # padding
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=0)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white', text='Autor:', font=20) \
            .grid(row=1, column=0, padx=(0, 1100))
        self.__autor = tk.Text(self.glavni_prozor, height=1, width=50, font=10)
        self.__autor.config(state='disabled', bg='#3F4C5C', foreground='white')
        self.__autor.grid(row=1, column=0, padx=(0, 600), pady=10)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white', text='Datum objavljivanja:', font=20) \
            .grid(row=2, column=0, padx=(0, 1010))
        self.__datum = tk.Text(self.glavni_prozor, height=1, width=50, font=10)
        self.__datum.config(state='disabled', bg='#3F4C5C', foreground='white')
        self.__datum.grid(row=2, column=0, padx=(0, 410), pady=10)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white', text='Osjećanje:', font=20) \
            .grid(row=2, column=0, padx=(750, 0))
        self.__osjecanje = tk.Text(self.glavni_prozor, height=1, width=20, font=10)
        self.__osjecanje.config(state='disabled', bg='#3F4C5C', foreground='white')
        self.__osjecanje.grid(row=2, column=0, padx=(1025, 0))

        # padding
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=5)
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=6)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white', text='Naslov', font=30) \
            .grid(row=7, column=0, sticky='nsew')
        self.__naslov = tk.Text(self.glavni_prozor, height=2, width=100, font=10)
        self.__naslov.config(state='disabled', bg='#3F4C5C', foreground='white')
        self.__naslov.grid(row=8, column=0, padx=10, pady=10)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white', text='Sažetak', font=20) \
            .grid(row=9, column=0, sticky='nsew')
        self.__rezime = tk.Text(self.glavni_prozor, height=13, width=125, font=10)
        self.__rezime.config(state='disabled', bg='#3F4C5C', foreground='white')
        self.__rezime.grid(row=10, column=0, padx=10, pady=10)

        # padding
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=11)
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=12)

        tk.Label(self.glavni_prozor, bg='#1D2733', foreground='white',
                 text='  Filtrirajte tekst unošenjem riječi razdvojenih zarezima:', font=15) \
            .grid(row=13, column=0, padx=(0, 800))
        tk.Checkbutton(self.glavni_prozor, bg='#1D2733', variable=self.__filtriranje_ukljuci,
                       command=self.__ukljuci_iskljuci_filtriranje).grid(row=13, column=0, sticky='w')

        self.__filtriranje = tk.Text(self.glavni_prozor, foreground='white', height=1, width=100)
        self.__filtriranje.config(state='disabled', bg='#3F4C5C')
        self.__filtriranje.grid(row=13, column=0, padx=(400, 0), pady=10)

        # padding
        tk.Label(self.glavni_prozor, bg='#1D2733').grid(row=14)

        tk.Label(self.glavni_prozor, foreground='white', bg='#1D2733', text='URL', font=30) \
            .grid(row=15, column=0, sticky='nsew')
        self.__url = tk.Text(self.glavni_prozor, bg='#112D4A', foreground='white', height=1, width=150)
        self.__url.grid(row=16, column=0, padx=10, pady=10)
        tk.Checkbutton(self.glavni_prozor, bg='#1D2733', font=15,
                       variable=self.__clanak.vise_clanaka, ).grid(row=17, column=0, padx=(0, 125))
        tk.Label(self.glavni_prozor, foreground='white', bg='#1D2733', text="Obradite više članaka", font=15) \
            .grid(row=17, column=0, padx=(50, 0))

        tk.Button(self.glavni_prozor, bg='#3A6AA5', text='Obradi!', command=self.lokalna_obrada) \
            .grid(row=18, column=0, padx=10, pady=10)

        self.glavni_prozor.configure(bg='#1D2733')
        self.glavni_prozor.mainloop()

    def __ukljuci_iskljuci_filtriranje(self) -> None:
        if self.__filtriranje_ukljuci.get():
            self.__filtriranje.config(state='normal', bg='#112D4A')
        else:
            self.__filtriranje.config(state='disabled', bg='#3F4C5C')

    def __filtriraj(self):
        lista_za_filtriranje = self.__filtriranje.get('1.0', 'end').strip().split(',')
        tekst = self.__clanak.moj_clanak.text.lower()
        if lista_za_filtriranje[0] != '':
            if any(rijec.lower() in tekst for rijec in lista_za_filtriranje):
                self.prozor_filtriraj()
                if not self.__da_ne.get():
                    self.__dozvoli_unos()
                    self.__obrisi()
                    self.__ukini_dozvolu_unosa()
                    self.__filtriranje_zavrseno.set(False)
                    return True
                else:
                    self.__filtriranje_zavrseno.set(False)
                    return False
        return False

    def __obrisi(self) -> None:
        self.__naslov.delete('1.0', 'end')
        self.__autor.delete('1.0', 'end')
        self.__datum.delete('1.0', 'end')
        self.__rezime.delete('1.0', 'end')
        self.__osjecanje.delete('1.0', 'end')

    def __dozvoli_unos(self) -> None:
        self.__naslov.config(state='normal')
        self.__autor.config(state='normal')
        self.__datum.config(state='normal')
        self.__rezime.config(state='normal')
        self.__osjecanje.config(state='normal')

    def __ukini_dozvolu_unosa(self) -> None:
        self.__naslov.config(state='disabled')
        self.__autor.config(state='disabled')
        self.__datum.config(state='disabled')
        self.__rezime.config(state='disabled')
        self.__osjecanje.config(state='disabled')

    def lokalna_obrada(self) -> None:
        url = self.__url.get('1.0', 'end').strip()

        if not self.__clanak.validan_url(url):
            self.__dozvoli_unos()
            self.__obrisi()
            self.__ukini_dozvolu_unosa()
            messagebox.showerror(title="URL Greska", message="Molimo Vas unesite validan URL")
            return

        if self.__clanak.vise_clanaka.get():
            self.lokalna_obrada_vise_clanaka()
            return

        self.__clanak.obrada(url)

        if self.__filtriraj():
            return

        self.__dozvoli_unos()

        self.__obrisi()

        self.__naslov.insert('1.0', self.__clanak.moj_clanak.title)

        self.__autor.insert('1.0', (self.__clanak.moj_clanak.authors if len(self.__clanak.moj_clanak.authors) != 0
                                    else "Nepoznati autor"))

        self.__datum.insert('1.0', str(self.__clanak.moj_clanak.publish_date) if self.__clanak.moj_clanak.publish_date
                                                                                 is not None else "Nepoznati datum")

        self.__rezime.insert('1.0', self.__clanak.moj_clanak.summary)

        self.__osjecanje.insert('1.0', "Pozitivno" if self.__clanak.analiza.polarity > 0 else "Neutralno"
                                                    if self.__clanak.analiza.polarity == 0 else "Negativno")

        self.__ukini_dozvolu_unosa()

    def lokalna_obrada_vise_clanaka(self) -> None:
        self.__lista_clanaka = self.__clanak.obrada_vise_clanaka(self.__url.get('1.0', 'end').strip())
        self.__clanak.set_vise_clanaka(False)
        if len(self.__lista_clanaka) == 0:
            messagebox.showerror(title="Greska pri obradi", message="Nismo uspjeli da pronađemo članke na zadatom "
                                                                    "linku. Molimo pokušajte ponovo.")
            return

        self.__sledeci = tk.Button(self.glavni_prozor, bg='#3A6AA5', text='Sledeći', command=self.__povecaj)
        self.__sledeci.grid(row=19, column=0, padx=10, pady=10, sticky='e')

        self.__manipulacija_url()
        self.lokalna_obrada()

    def __umanji(self) -> None:
        self.__trenutni.set(self.__trenutni.get() - 1)
        # ukini prethodnog
        if self.__trenutni.get() - 1 < 0 and self.__prethodni is not None:
            self.__prethodni.destroy()
            self.__prethodni = None
        # pojavljivanje sledeceg
        if self.__trenutni.get() + 1 <= len(self.__lista_clanaka) - 1:
            if self.__sledeci is None:
                self.__sledeci = tk.Button(self.glavni_prozor, bg='#3A6AA5', text='Sledeći', command=self.__povecaj)
                self.__sledeci.grid(row=19, column=0, padx=10, pady=10, sticky='e')
        if self.__trenutni.get() >= 0:
            self.__manipulacija_url()
            self.lokalna_obrada()
        else:
            self.__trenutni.set(self.__trenutni.get() + 1)

    def __povecaj(self) -> None:
        self.__trenutni.set((self.__trenutni.get() + 1))
        # ukini sledeci
        if self.__trenutni.get() + 1 > len(self.__lista_clanaka) - 1 and self.__sledeci is not None:
            self.__sledeci.destroy()
            self.__sledeci = None
        # pojavljivanje prethodnog
        if self.__trenutni.get() - 1 >= 0:
            if self.__prethodni is None:
                self.__prethodni = tk.Button(self.glavni_prozor, bg='#3A6AA5', text='Prethodni', command=self.__umanji)
                self.__prethodni.grid(row=19, column=0, padx=10, pady=10, sticky='w')
        if self.__trenutni.get() <= len(self.__lista_clanaka) - 1:
            self.__manipulacija_url()
            self.lokalna_obrada()
        else:
            self.__trenutni.set(self.__trenutni.get() - 1)

    def __manipulacija_url(self) -> None:

        self.__url.delete('1.0', 'end')
        self.__url.insert('1.0', self.__lista_clanaka[self.__trenutni.get()])

    def prozor_filtriraj(self) -> None:
        toplevel = tk.Toplevel(self.glavni_prozor)

        toplevel.title("Filtriranje")
        toplevel.geometry("410x140")

        l1 = tk.Label(toplevel, image="::tk::icons::question")
        l1.grid(row=0, column=0, padx=(30, 0), pady=(30, 0))
        l2 = tk.Label(toplevel, text='Obrađena vijest sadrži neke od pojmova koje ste unijeli'
                                     ' za filtriranje. Da li ipak želite da nastavite sa čitanjem?', wraplength=300)
        l2.grid(row=0, column=1, padx=(5, 0), pady=(30, 0))

        b1 = tk.Button(toplevel, text="Da", command=self.postavi_da, width=10)
        b1.grid(row=1, column=1, sticky='w', pady=(20, 0))
        b2 = tk.Button(toplevel, text="Ne", command=self.postavi_ne, width=10)
        b2.grid(row=1, column=1, sticky='e', pady=(20, 0))

        self.glavni_prozor.wait_variable(self.__filtriranje_zavrseno)
        toplevel.destroy()

    def postavi_da(self) -> None:
        self.__da_ne.set(True)
        self.__filtriranje_zavrseno.set(True)

    def postavi_ne(self) -> None:
        self.__da_ne.set(False)
        self.__filtriranje_zavrseno.set(True)
