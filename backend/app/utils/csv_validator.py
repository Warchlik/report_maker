"id,data,cena_netto,cena_brutto,waluta,stawka_vat,ilosc,kategoria"

from pathlib import Path
from app.core.config import REPORTS_DIR
import pandas as pd


SUFFIX = {
    "data": ["data", "date"],
    "cena_netto": ["ammount_netto", "netto"],
    "cena_butto": ["cena_brutto", "brutto", "amount_brutto"],
    "waluta": ["waluta", "currency"],
    "stawka_vat": ["stawka_vat", "vat", "%"],
    "ilość": ["quatity", "ilosc", "ilość", "ilość_przedmiotów"],
    "kategoria": ["category", "kategoria"],
}


def generate_report(owner: int, filename: str):
    path_to_file: Path = REPORTS_DIR / str(owner) / filename

    df = pd.read_csv(path_to_file, header=0)

    # TODO: dokonczyć funkcjonalności workera
    maped_df = _map_columns(df)
    pass


def _map_columns(data_frame: pd.DataFrame):
    data_frame.columns = data_frame.columns.str.lower().str.strip()

    column_mapping = {}
    for name, aliases in SUFFIX.items():
        for alias in aliases:
            column_mapping[alias] = name

    data_frame.rename(columns=column_mapping, inplace=True)
    existing_columns = set(SUFFIX.keys()).intersection(data_frame.columns)

    final_df = data_frame[list[existing_columns]]

    report_data = final_df.to_dict(orient="records")

    return report_data
