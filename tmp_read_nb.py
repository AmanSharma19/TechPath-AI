import json

with open('notebooks/01_data_cleaning_eda.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
    
with open('tmp_nb_out.txt', 'w', encoding='utf-8') as f_out:
    for i, cell in enumerate(nb['cells']):
        f_out.write(f"--- Cell {i} ({cell['cell_type']}) ---\n")
        source = "".join(cell.get('source', []))
        f_out.write(source + "\n")
