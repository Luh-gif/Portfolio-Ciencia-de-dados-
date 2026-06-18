import pandas as pd
import glob
import os

files = glob.glob('Senior/Projeto Senior 09 - Geology Prediction/data/raw/train/*__typewell.csv')
counts = {'has_labels': 0, 'empty': 0}
labels_found = set()

for f in files:
    try:
        df = pd.read_csv(f)
        if 'Geology' in df.columns and not df['Geology'].dropna().empty:
            counts['has_labels'] += 1
            labels_found.update(df['Geology'].dropna().unique())
        else:
            counts['empty'] += 1
    except Exception as e:
        print(f"Erro no arquivo {f}: {e}")

print(f"Total de arquivos analisados: {len(files)}")
print(f"Arquivos com labels: {counts['has_labels']}")
print(f"Arquivos sem labels: {counts['empty']}")
print(f"Labels únicos encontrados: {labels_found}")
