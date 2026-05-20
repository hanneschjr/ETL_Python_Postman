import pandas as pd
import os

def save(dir_files, sheets, names_sheets):
    for sheet, name_sheet in zip(sheets, names_sheets):
        dataframe = pd.DataFrame(sheet)
        file = os.path.join(dir_files, f"{name_sheet}.csv")
        dataframe.to_csv(path_or_buf=file,sep=';', index=False)