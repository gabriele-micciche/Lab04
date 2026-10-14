import csv

class Espositori:
    def __init__(self, codice_espositore, nome, cognome):
        self.__codice_espositore = codice_espositore
        self.__nome = nome
        self.__cognome = cognome
    @property
    def codice(self):
        return self.__codice_espositore
    @property
    def nome(self):
        return self.__nome
    @property
    def cognome(self):
        return self.__cognome

    def __str__(self):
        return f"Codice {self.__codice_espositore}, {self.__nome}, {self.__cognome}"

class Stand:
    def __init__(self, codice_stand, superficie, padiglione, prezzo):
        self.__codice_stand = codice_stand
        self.__superficie = superficie
        self.__padiglione = padiglione
        self.__prezzo = prezzo


    @property
    def codice(self):
        return self.__codice_stand
    @property
    def superficie(self):
        return self.__superficie
    @property
    def padiglione(self):
        return self.__padiglione
    @property
    def prezzo(self):
        return self.__prezzo

    def __str__(self):
        return f"{self.__codice_stand}, {self.__superficie}, {self.__padiglione}, {self.__prezzo}"

class Prese(Stand):
    def __init__(self, codice_stand, superficie, padiglione, prezzo, prese):
        super().__init__(codice_stand, superficie, padiglione, prezzo)
        self.__prese = prese

    @property
    def prese(self):
        return self.__prese

    def __str__(self):
        return f"{super().__str__()}, {self.prese}"


class Premium(Stand):
    def __init__(self, codice_stand, superficie, padiglione, prezzo, posizione):
        super().__init__(codice_stand, superficie, padiglione, prezzo)
        self.__posizione = posizione

    @property
    def posizione(self):
        return self.__posizione

    def __str__(self):
        return f"{super().__str__()}, {self.__posizione}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.espositori = {}
        self.stand = {}
        self.prestiti = {}

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                for line in reader:
                    if line[0].startswith("E"):
                        codice = line[0]
                        nome = line[1]
                        cognome = line[2]
                        espositore = Espositori(codice, nome, cognome)
                        self.espositori[codice] = espositore

                    if line[0].startswith("S") and len(line) == 4:
                        codice = line[0]
                        superficie = line[1]
                        padiglione = line[2]
                        prezzo = line[3]
                        stand = Stand(codice, superficie, padiglione, prezzo)
                        self.stand[codice] = stand

                    if line[0].startswith("S") and len(line) == 5:
                        codice = line[0]
                        superficie = line[1]
                        padiglione = line[2]
                        prezzo = line[3]
                        valore = line[4]
                        if valore.isdigit():
                            presa_elettrica = int(valore)
                            prese = Prese(codice, superficie, padiglione, prezzo, presa_elettrica)
                            self.stand[codice] = prese
                        else:
                            posizione = valore
                            premium = Premium(codice, superficie, padiglione, prezzo, posizione)
                            self.stand[codice] = premium

        except FileNotFoundError:
            raise Exception(f"File {file_path} non trovato")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand:
            raise Exception(f"Stand {codice_stand} non trovato")
        if codice_espositore not in self.espositori:
            raise Exception(f"Espositore {codice_espositore} non trovato")

        # Controllo se lo stand è già occupato
        if codice_stand in self.prestiti:
            raise Exception("Lo stand è già in prestito")

        # Controllo se l'espositore ha già un altro stand assegnato
        for x in self.prestiti.values():
            if x.codice == codice_espositore:
                raise Exception("L'espositore non è disponibile")

        if codice_stand not in self.prestiti:
            prestito = Espositori(codice_espositore, None, None)
            self.prestiti[codice_stand] = prestito
        return self.prestiti
    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """


    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO
