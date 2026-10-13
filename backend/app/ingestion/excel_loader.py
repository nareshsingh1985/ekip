import pandas as pd

def load_excel(file_path: str):

    sheets = pd.read_excel(
        file_path,
        sheet_name=None
    )

    content = []

    for sheet_name, df in sheets.items():
        content.append(
            f"\nSheet: {sheet_name}\n"
        )

        content.append(
            df.to_string(index=False)
        )

    return "\n".join(content)