import os
import pandas as pd

def split_csv(input_file, output_dir, n_splits=5):
    print(f"Lendo arquivo: {input_file}")
    
    # Usando chunksize para não carregar tudo na memória de uma vez, 
    # embora 500MB caibam na maioria das máquinas, é uma boa prática sênior.
    chunk_list = []
    for chunk in pd.read_csv(input_file, chunksize=1000000):
        chunk_list.append(chunk)
    
    df = pd.concat(chunk_list)
    total_rows = len(df)
    rows_per_split = total_rows // n_splits
    
    print(f"Total de linhas: {total_rows}")
    print(f"Linhas por arquivo: {rows_per_split}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i in range(n_splits):
        start_idx = i * rows_per_split
        # O último arquivo pega o restante
        end_idx = (i + 1) * rows_per_split if i < n_splits - 1 else total_rows
        
        split_df = df.iloc[start_idx:end_idx]
        output_file = os.path.join(output_dir, f"paysim_part_{i+1}.csv")
        split_df.to_csv(output_file, index=False)
        print(f"Salvo: {output_file}")

if __name__ == "__main__":
    input_path = r"c:\Users\luizn\OneDrive\Documentos\Analises-de-Dados\PaySim mobile - Data Base - Copia.csv"
    output_path = r"c:\Users\luizn\OneDrive\Documentos\Analises-de-Dados\PaySim_SQL_Project\data\raw"
    split_csv(input_path, output_path)
