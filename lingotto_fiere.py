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

    def __eq__(self, other):
        if isinstance(other, Espositori):
            return self.__codice_espositore == other.codice
        return False

    def __str__(self):
        return f"Codice {self.__codice_espositore}: {self.__nome} {self.__cognome}"

class Stand:
    def __init__(self, codice_stand, superficie, padiglione, prezzo):
        self.__codice_stand = codice_stand
        self.__superficie = superficie
        self.__padiglione = padiglione
        self.__prezzo = prezzo
        self.__disponibile = True
        self.__espositore = None


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

    @property
    def disponibile(self):
        return self.__disponibile

    @disponibile.setter
    def disponibile(self, valore):
        self.__disponibile = valore

    @property
    def espositore(self):
        return self.__espositore

    @espositore.setter
    def espositore(self, espositore):
        self.__espositore = espositore

    def __lt__(self, other):
        return self.prezzo < other.prezzo

    def __str__(self):
        return f"{self.__codice_stand}, {self.__superficie}, {self.__padiglione}, {self.__prezzo}"

class Prese(Stand):
    def __init__(self, codice_stand, superficie, padiglione, prezzo, prese):
        super().__init__(codice_stand, superficie, padiglione, prezzo)
        self.__prese = prese

    @property
    def prese(self):
        return self.__prese

    @property
    def prezzo(self):
        return super().prezzo * (1 + 0.07 * self.__prese)

    def __str__(self):
        return f"{super().__str__()}, {self.prese}"


class Premium(Stand):
    def __init__(self, codice_stand, superficie, padiglione, prezzo, posizione):
        super().__init__(codice_stand, superficie, padiglione, prezzo)
        self.__posizione = posizione

    @property
    def posizione(self):
        return self.__posizione

    @property
    def prezzo(self):
        return super().prezzo * 1.30

    def __str__(self):
        return f"{super().__str__()}, {self.__posizione}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.espositori = {}
        self.stand = {}

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
                        prezzo = float(line[3])
                        stand = Stand(codice, superficie, padiglione, prezzo)
                        self.stand[codice] = stand

                    if line[0].startswith("S") and len(line) == 5:
                        codice = line[0]
                        superficie = line[1]
                        padiglione = line[2]
                        prezzo = float(line[3])
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

        stand = self.stand[codice_stand]
        espositore = self.espositori[codice_espositore]

        # Controllo disponibilità dello stand
        if stand.disponibile == False:
            raise Exception("Lo stand è già assegnato")

        # Controllo se l'espositore ha già un altro stand
        for s in self.stand.values():
            if s.espositore == espositore:
                raise Exception("L'espositore non è disponibile")

        # Assegnazione reale richiesta dalla traccia
        stand.espositore = espositore
        stand.disponibile = False

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for i in self.espositori.values():
            # Cerchiamo se c'è uno stand associato a questo espositore
            stand_trovato = None
            for s in self.stand.values():
                if s.espositore is not None and s.espositore.codice == i.codice:
                    stand_trovato = s
                    break

            if stand_trovato is not None:
                print(f"{i} - Stand: {stand_trovato.codice}")
            else:
                print(f"{i} - Nessuno stand associato")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand.values())