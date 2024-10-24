import pandas as pd
from Bio import SeqIO
import re
import sys

# Funzione per leggere il file di input e il file FASTA
def associa_ind_sequenza(file_dati, file_fasta):
    # Inizializza un dizionario per tenere traccia delle associazioni
    ind_popuid = {}

    # Espressione regolare per catturare le righe rilevanti nel file di input
    pattern_ind = re.compile(r'^>Summary for (Ind\d+)')
    pattern_haplo = re.compile(r'^Keeping Haplo (PopUID\.\d+) : ([\d.]+)')
    
    # Leggi il file di input
    with open(file_dati, 'r') as f:
        current_ind = None
        for line in f:
            line = line.strip()
            # Cerca l'individuo corrente
            match_ind = pattern_ind.match(line)
            if match_ind:
                current_ind = match_ind.group(1)
                ind_popuid[current_ind] = []
            # Cerca l'aplotipo corrispondente per l'individuo corrente
            elif current_ind:
                match_haplo = pattern_haplo.match(line)
                if match_haplo:
                    popuid = match_haplo.group(1)
                    valore = float(match_haplo.group(2))
                    # Aggiungi l'aplotipo e il valore all'individuo corrente
                    ind_popuid[current_ind].append((popuid, valore))
    
    # Leggi il file FASTA
    fasta_sequenze = SeqIO.to_dict(SeqIO.parse(file_fasta, "fasta"))

    # Associa ogni individuo a tutte le sequenze dei PopUID corrispondenti
    ind_sequenze = {}
    for ind, popuids in ind_popuid.items():
        sequenze = []
        # Trova tutte le sequenze associate ai PopUID dell'individuo
        for popuid, valore in popuids:
            if popuid in fasta_sequenze:
                sequenza = str(fasta_sequenze[popuid].seq)
                sequenze.append(f">{ind}_{popuid}\n{sequenza}")
            else:
                print(f"Attenzione: PopUID {popuid} non trovato per {ind}")
        
        # Unisci le sequenze trovate
        if sequenze:
            ind_sequenze[ind] = "\n".join(sequenze)
        else:
            ind_sequenze[ind] = "None"

    return ind_sequenze

# File input
file_dati = sys.argv[1]
file_fasta = sys.argv[2]

# Associa le sequenze agli Ind
associazioni = associa_ind_sequenza(file_dati, file_fasta)

# Stampa le associazioni
for ind, sequenza in associazioni.items():
    print(f"{sequenza}")
