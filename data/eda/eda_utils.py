def transform_csv_row(row): # Function to transform a single row of data from de dataset
                            # df = df.apply(transform_row, axis=1)
    row['Age'] = int(row['Age']) # Age in years
    row['Height'] = int(row['Height'] * 100) # Height in cm
    row['Weight'] = int(row['Weight'] * 100) # Weight in gr
    # Cast back weight to kg and height to m para calculate BMI
    height_m = row['Height'] / 100  # convertimos cm a m
    weight_kg = row['Weight'] / 1000  # convertimos gramos a kg
    row['BMI'] = round(weight_kg / (height_m ** 2), 2)

    # Binary yes/no columns to bool
    yes_no_cols = ['family_history_with_overweight', 'FAVC', 'SMOKE', 'SCC'] # , 'CALC'
    for col in yes_no_cols:
        val = row[col].strip().lower()
        if val == 'yes':
            row[col] = True
        elif val == 'no':
            row[col] = False
        else:
            raise ValueError(f"Invalid value for {col}: {row[col]}")

    row['FCVC'] = int(row['FCVC'])
    row['NCP'] = int(row['NCP'])
    row['CH2O'] = int(row['CH2O'] * 100)
    row['FAF'] = int(row['FAF'])
    row['TUE'] = int(row['TUE'] * 60)

    return row
