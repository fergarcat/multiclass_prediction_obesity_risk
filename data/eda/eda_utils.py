def transform_csv_row(row):
    row['Age'] = int(row['Age'])  # Age in years

    # BMI calculation
    row['BMI'] = round(weight / (height ** 2), 2)

    # Binary yes/no to bool
    yes_no_cols = ['family_history_with_overweight', 'FAVC', 'SCC']
    for col in yes_no_cols:
        val = row[col].strip().lower()
        if val == 'yes':
            row[col] = True
        elif val == 'no':
            row[col] = False
        else:
            raise ValueError(f"Invalid value for {col}: {row[col]}")

    # Gender
    if row['Gender'].strip().lower() == 'male':
        row['Gender'] = 1
    else:
        row['Gender'] = 0

    # Resto de columnas
    row['FCVC'] = int(row['FCVC'])
    row['NCP'] = int(row['NCP'])
    row['CH2O'] = int(row['CH2O'] * 100)
    row['FAF'] = int(row['FAF'])
    row['TUE'] = int(row['TUE'] * 60)

    # Convertir booleanos a enteros
    for col in yes_no_cols:
        row[col] = int(row[col])

    return row
