import random
from functools import cmp_to_key

'''
L'idea è quella di vedere un'offerta come un cromosoma, dove i geni sono la codifica binaria della presenza o meno, nell'offerta stessa, dell'oggetto in questione.
L'individuo sarà l'insieme di cromosomi (offerte codificate) compatibili tra loro secondo i vincoli imposti dalla definizione di asta combinatoria.
Ad ogni cromosoma, viene assegnata una funzione di valutazione (budget)
'''

# Parametri dell'asta
oggetti = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
acquirenti = [
    'Alice', 'Bob', 'Charlie', 'Martin', 'Jhon', 'Simon', 'Thomas', 'Harry', 'Jack', 'Oscar', 'James', 'William',
    'Sara', 'Ethan'
]

offerte = {
    'Alice': ['A', 'B'],
    'Bob': ['B', 'C'],
    'Charlie': ['C', 'D'],
    'Martin': ['A', 'E', 'I'],
    'Jhon': ['B', 'H'],
    'Simon': ['B', 'C', 'E'],
    'Thomas': ['A', 'B', 'C'],
    'Harry': ['A', 'F'],
    'Jack': ['F', 'G'],
    'Oscar': ['C', 'D', 'F', 'G'],
    'James': ['C', 'E', 'H'],
    'William': ['A', 'D'],
    'Sara': ['F'],
    'Ethan': ['I']
}

budget = {
    'Alice': 50,
    'Bob': 60,
    'Charlie': 75,
    'Martin': 25,
    'Jhon': 70,
    'Simon': 50,
    'Thomas': 90,
    'Harry': 35,
    'Jack': 65,
    'Oscar': 90,
    'James': 50,
    'William': 50,
    'Sara': 65,
    'Ethan': 45,
}


# Parametri dell'algoritmo genetico
num_popolazione_iniziale = 5
num_genitori_selezionati = 2
num_figli_generati_da_genitori = 10
probabilita_cross_over = 0.8
probabilita_mutazione = 0.5
num_iterazioni = 10


'''
Definiamo una rappresentazione delle soluzioni come un vettore binario di lunghezza pari al numero di oggetti in vendita.
Ad esempio, se abbiamo gli oggetti A, B, C, D, E, una soluzione potrebbe essere rappresentata come [1, 0, 1, 0, 1], indicando che gli oggetti A, C e E sono selezionati per l'offerta.
'''
def codifica_offerte():
    offerte_codificate = []

    for p in offerte:
        preferenza_codificata = []

        for i, n in enumerate(oggetti):
            if n in offerte[p]:
                preferenza_codificata.append(1)
            else:
                preferenza_codificata.append(0)

        offerte_codificate.append(preferenza_codificata)

    return offerte_codificate

'''
Decodifichiamo la rappresentazione dell'offerta in forma iniziale
'''
def decodifica_offerta(offerta):
    decodifica = []

    for i, e in enumerate(oggetti):
        if offerta[i] == 1:
            decodifica.append(e)

    return decodifica

'''
Controlla la compatibilità di due offerte: es. se vengono richieste due volte lo stesso oggetto A le offerte non possono essere soddisfatte allo stesso tempo
'''
def controlla_compatibilità_offerta(offerta_1, offerta_2):
    compatibile = True
    indici_selezionati = []

    for i, e in enumerate(offerta_1):
        if e == 1:
            indici_selezionati.append(i)

    for i in indici_selezionati:
        if offerta_2[i] == 1:
            compatibile = False
    # print("Confronta: " + str(offerta_1) + " " + str(offerta_2)+" -> "+str(indici_selezionati)+" -> "+str(compatibile))
    return compatibile


'''
Creaiamo una soluzione iniziale rispettando i vincoli imposti dall'asta combinatoria
'''
def genera_soluzione_iniziale(offerte_codificate):
    soluzione = []
    rand_i = random.randint(0, len(offerte_codificate)-1)
    soluzione.append(offerte_codificate[rand_i])

    for i, n in enumerate(offerte_codificate):
        compatibile = True
        for s in soluzione:
            if controlla_compatibilità_offerta(s, n):
                compatibile = True
                continue
            else:
                compatibile = False
                break
        if compatibile:
            rand_m = random.random()
            if rand_m < probabilita_mutazione:
                soluzione.append(n)

    return soluzione

'''
Creaiamo una soluzione rispettando i vincoli imposti dall'asta combinatoria
'''
def genera_soluzione(genitori, offerte_codificate):
    soluzione = []

    #Trova i geni dei genitori compatibili tra loro (vincolo asta cambinatoria
    for g in genitori:
        rand_i = random.randint(0, len(g[0])-1)
        compatibile = True
        for s in soluzione:
            if controlla_compatibilità_offerta(s, g[0][rand_i]):
                compatibile = True
                continue
            else:
                compatibile = False
                break
        if compatibile:
            rand_p = random.random()
            if rand_p < probabilita_cross_over:
                soluzione.append(g[0][rand_i])

    #Introduciamo aleatoriamente nuovo materiale genetico con una mutazione inserendo altri geni da offerte codificate compatibili con i geni ereditati dai genitori
    for i, n in enumerate(offerte_codificate):
        compatibile = True
        for s in soluzione:
            if controlla_compatibilità_offerta(s, n):
                compatibile = True
                continue
            else:
                compatibile = False
                break
        if compatibile:
            rand_m = random.random()
            if rand_m < probabilita_mutazione:
                soluzione.append(n)

    return soluzione

'''
Creiamo una popolazione iniziale di soluzioni casuali.
Ogni soluzione deve rispettare il vincolo che le offerte siano atomiche e non frazionabili.
Assicuriamoci che la popolazione abbia una diversità sufficiente per consentire una ricerca efficace.
'''
def genera_popolazione_inziale(offerte_codificate, num_popolazione_iniziale):
    popolazione = []

    for _ in range(num_popolazione_iniziale):
        soluzione_iniziale = genera_soluzione_iniziale(offerte_codificate)
        if soluzione_iniziale not in popolazione:
            popolazione.append(soluzione_iniziale)

    print("- Popolazione iniziale: "+str(popolazione))
    return popolazione


'''
Utilizziamo questa funzione per ordinare due individui in base al relativo valore di fitness
'''
def compara_individui(individuo1, individuo2):
    if individuo1[1] < individuo2[1]:
        return 1
    elif individuo1[1] > individuo2[1]:
        return -1
    else:
        return 0
'''
Calcoliamo il valore totale delle offerte per ogni soluzione nella popolazione.
Utilizziamo le informazioni sulle offerte degli agenti per calcolare il valore totale corrispondente a ciascuna soluzione.
'''
def calcolo_max_fitness_popolazione_corrente(popolazione, debug=False):
    valore_offerta_max = 0
    offerta_max = []
    popolazione_con_fitness = []

    if debug:
        print("\n- Calcolo il valore di fitness per la popolazione attuale:")

    for o in popolazione:
        valore_offerta = 0
        offerte_decodificate = []
        for e in o:
            # Decodifico l'offerta corrente della popolazione attuale
            offerta_decodificata = decodifica_offerta(e)
            offerte_decodificate.append(offerta_decodificata)

            # Ottengo il budget massimo per l'offerta totale
            for p in offerte:
                if offerte[p] == offerta_decodificata:
                    valore_offerta += budget[p]

            # Inserisco l'individuo con il suo valore di fitness nella lista
            popolazione_con_fitness.append([o, valore_offerta])

            # Congronto il valore corrente con il massimo globale
            if valore_offerta > valore_offerta_max:
                valore_offerta_max = valore_offerta
                offerta_max = offerte_decodificate
        if debug:
            print(str(o)+" vale "+str(valore_offerta)+"$")

    # Stampo il massimo per il calcolo del fitness della popolazione attuale
    if debug:
        print("--- L'offerta massima è attualmente "+str(offerta_max)+" con valore totale di "+str(valore_offerta_max)+"$")

    # Ordino il risultato per fitness decrescente
    popolazione_con_fitness = sorted(popolazione_con_fitness, key=cmp_to_key(compara_individui))
    #for i in popolazione_con_fitness:
    #    print(str(i[1]))
    return popolazione_con_fitness


'''
Applichiamo operatori genetici come il cross-hover e la mutazione per generare nuovi individui dai genitori selezionati.
Assicuriamoci che i figli generati rispettino il vincolo delle offerte non frazionabili.
'''
def generazione_figlio(genitori, offerte_codificate):
    figlio = genera_soluzione(genitori, offerte_codificate)
    return figlio


'''
Selezioniamo un numero di soluzioni dalla popolazione corrente come genitori per la successiva generazione.
Possiamo utilizzare un metodo di selezione basato sulla fitness, come la selezione proporzionale o la selezione per torneo.
'''
def selezione_genitori(popolazione_corrente):
    print("- Selezioniamo un numero di individui migliori dalla popolazione corrente come genitori per la successiva generazione.")

    popolazione_ordinata = calcolo_max_fitness_popolazione_corrente(popolazione_corrente)
    genitori = []

    for i in range(num_genitori_selezionati):
        genitori.append(popolazione_ordinata[i])

    for j in range(len(genitori)):
        print("Genitore "+str(j+1)+": "+str(genitori[j]))

    return genitori


def algoritmo_genetico(popolazione_corrente, offerte_codificate):
    nuova_generazione = popolazione_corrente

    for iterazione in range(num_iterazioni):
        print("\n------ Avviamo la "+str(iterazione+1)+"a iterazione dell'algoritmo generico ------")

        # Selezioniamo i migliori individui come genitori e inseriamoli nella popolazione corrente
        genitori = selezione_genitori(nuova_generazione)
        nuova_generazione = []
        for g in genitori:
            nuova_generazione.append(g[0])

        print("\n- Generiamo "+str(num_figli_generati_da_genitori)+" figli da una scelta casuale di geni dei migliori individui selezionati.")
        for i in range(num_figli_generati_da_genitori):
            figlio = generazione_figlio(genitori, offerte_codificate)
            if figlio not in nuova_generazione:
                nuova_generazione.append(figlio)

        print("- La nuova generazione di individui è: ")
        for n in nuova_generazione:
            print(str(n))

        calcolo_max_fitness_popolazione_corrente(nuova_generazione, True)


# Main function
def main():
    print("- Oggetti in vendita: "+str(oggetti))
    print("- Acquirenti: " + str(acquirenti))
    for p in offerte:
        print("- Offerta di "+p+" -> "+str(offerte[p])+" del valore di "+str(budget[p])+"$")

    #1
    offerte_codificate = codifica_offerte()
    print("- Codifica delle offerte: "+str(offerte_codificate))

    #2
    popolazione_iniziale = genera_popolazione_inziale(offerte_codificate, num_popolazione_iniziale)

    #3
    calcolo_max_fitness_popolazione_corrente(popolazione_iniziale, True)

    #4
    popolazione_corrente = popolazione_iniziale;
    algoritmo_genetico(popolazione_corrente, offerte_codificate)


if __name__ == '__main__':
    main()