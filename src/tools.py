import pandas as pd


def pandas_table(data: pd.DataFrame, transpose: bool = False) -> dict:
    """
    Recommended usage:
    ```python
    from nicegui import ui

    df = pd.DataFrame(<INIT-DATAFRAME>)
    data_d = pandas_table(df, transpose=True)
    data_d = set_aggrid_col_widths(data_d)

    grid = ui.aggrid(data_d)
    grid.options["suppressColumnVirtualization"] = True
    grid.update()
    ```
    """
    data = data.fillna("")
    if transpose:
        records = data.to_dict("list")
        col_num = None
        rowData = []
        for key, value in records.items():
            if not col_num:
                col_num = len(value)
            row_d = {"field": key.title()}
            for count, var in enumerate(value, start=1):
                row_d[f"person_{count}"] = var
            rowData.append(row_d)
        columnDefs = [{"headerName": "Fields", "field": "field"}]
        columnDefs.extend({"headerName": f"Person {i + 1}", "field": f"person_{i + 1}"} for i in range(col_num))
    else:
        rowData = data.to_dict("records")
        columnDefs = []
        for row in rowData:
            for header in row.keys():
                header_d = {"headerName": header.title(), "field": header.lower()}
                columnDefs.append(header_d)
            columnDefs = [dict(t) for t in {tuple(d.items()) for d in columnDefs}]
    return {"columnDefs": columnDefs, "rowData": rowData}


def set_aggrid_col_widths(data: dict) -> dict:
    """
    Recommended usage:
    ```python
    from nicegui import ui

    df = pd.DataFrame(<INIT-DATAFRAME>)
    data_d = pandas_table(df)
    data_d = set_aggrid_col_widths(data_d)

    grid = ui.aggrid(data_d)
    grid.options["suppressColumnVirtualization"] = True
    grid.update()
    ```
    """
    col_lengths = {}
    for rows in data["rowData"]:
        for col, value in rows.items():
            try:
                if col not in col_lengths:
                    col_lengths[col] = len(value)
                elif len(value) > len(col_lengths[col]):
                    col_lengths[col] = len(value)
            except TypeError as e:
                if "'datetime.datetime'" not in str(e):
                    raise TypeError(e) from e
                col_lengths[col] = 90

    for header in data["columnDefs"]:
        header_name_width = len(header["headerName"])
        print(header["headerName"], col_lengths[header["field"]], header_name_width, 8)
        size = max(col_lengths[header["field"]], header_name_width, 8)
        header["minWidth"] = size * 10
        header["maxWidth"] = size * 10
        header["suppressSizeToFit"] = True
    return data