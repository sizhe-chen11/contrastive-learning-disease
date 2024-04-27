#Imports
import pandas as pd
import numpy as np

#Derive fl_status column based on fl_echo and FLI(when available): 1 for positive; 0 for negative; -1 for unavailable
def derive_fl_status(row):
    # Derive FL_Check column to infer the status by echo or FLI
    liver_status = row['脂肪肝 fatty Liver (0:正常  1:mild 2:moderate 3:severe)']
    fli_value = row['FLI']

    if pd.isna(liver_status) and pd.isna(fli_value):
        return -1
    elif pd.notna(liver_status) and liver_status != 0:
        return 1
    elif pd.notna(fli_value) and fli_value >= 60:
        return 1
    else:
        return 0

def derive_MAFLD(df):
    df['MAFLD'] = 0  # Initialize MAFLD field as 0

    # Condition 1: fl_status = -1
    df.loc[df['fl_status'] == -1, 'MAFLD'] = -1

    # Condition 2: fl_check = 0
    df.loc[df['fl_status'] == 0, 'MAFLD'] = 0

    # Condition 3: fl_check = 1
    # Subcondition 1: BMI >= 23
    df.loc[(df['fl_status'] == 1) & (df['BMI'] >= 23), 'MAFLD'] = 1

    # Subcondition 2: BMI < 23 and mst >= 2
    df.loc[(df['fl_status'] == 1) & (df['BMI'] < 23) & (df['mst_total'] >= 2), 'MAFLD'] = 1

    # Subcondition 3: DM_determine = 1
    df.loc[(df['fl_status'] == 1) & (df['DM_determine'] == 1), 'MAFLD'] = 1

    return df

# We are now deriving target variables as MAFLD_0, MAFLD_Obesity, MAFLD_Diebetes, MAFLD_MD
def derive_MAFLD_with_multi_label(df):
    # Condition for non-case: derive MAFLD_0, if MAFLD is 0, then MAFLD_0 is 1, otherwise 0
    df['MAFLD_0'] = 0
    df.loc[df['MAFLD'] == 0, 'MAFLD_0'] = 1

    # Condition 1: MAFLD_Obesity, if MAFLD is 1 and BMI >= 23
    df['MAFLD_Obesity'] = 0
    df.loc[(df['MAFLD'] == 1) & (df['BMI'] >= 23), 'MAFLD_Obesity'] = 1

    # Condition 2: MAFLD_MD, if MAFLD is 1 and BMI < 23 and mst >= 2
    df['MAFLD_MD'] = 0
    df.loc[(df['MAFLD'] == 1) & (df['BMI'] < 23) & (df['mst_total'] >= 2), 'MAFLD_MD'] = 1

    # Condition 3: MAFLD_Diabetes, if MAFLD is 1 and DM_determine = 1
    df['MAFLD_Diabetes'] = 0
    df.loc[(df['MAFLD'] == 1) & (df['DM_determine'] == 1), 'MAFLD_Diabetes'] = 1

    # Additional Condition: if MAFLD is -1, set all labels to -1
    df.loc[df['MAFLD'] == -1, ['MAFLD_0', 'MAFLD_Obesity', 'MAFLD_MD', 'MAFLD_Diabetes']] = -1

    return df

# Sliding window function for multi_label
def sliding_window_multi_label_data(df, input_window_size, target_window_size):
    transformed_data = []
    group_counter = {}

    df_sorted = df.sort_values(['CMRC_id', 'year_come'])

    for patient_id, group in df_sorted.groupby('CMRC_id'):
        if len(group) < input_window_size + target_window_size:
            continue


        group_counter.setdefault(patient_id, 0)
        group_counter[patient_id] += 1
        group_alias = f'{patient_id}_group{group_counter[patient_id]}'

        for i in range(len(group) - input_window_size - target_window_size + 1):
            input_data = group[i:i+input_window_size]
            target_data = group[i+input_window_size:i+input_window_size+target_window_size]

            # Flatten input_data and repeat target_data
            input_features_t1 = input_data.iloc[0, :].values.flatten()
            target_columns = [f't2_{col}' for col in target_data.columns]
            new_row = [group_alias] + list(input_features_t1) + list(target_data.values[0])
            transformed_data.append(new_row)

    columns_list = ['CMRC_id'] + [f't1_{col}' for col in input_data.columns] + [f't2_{col}' for col in target_data.columns]
    transformed_df = pd.DataFrame(transformed_data, columns=columns_list)
    return transformed_df

def add_prefix(cols, prefixes):
# Note the prefixes should be a LIST, eg. prefixes = ["t1_", "t2_"]
    renamed_columns = []
    for prefix in prefixes:
        renamed_columns.extend([prefix + column for column in cols])
    return renamed_columns

def null_ratio(row):
    return row.isnull().sum() / len(row)

def select_record(group):
    group['null_ratio'] = group.apply(null_ratio, axis=1)
    min_null_ratio = group['null_ratio'].min()
    group = group[group['null_ratio'] == min_null_ratio]
    selected_record = group.loc[group['t1_year_come'].idxmin()]
    return selected_record.to_frame().T


def process_label_powerset(y_labels, y_labels_lp):
    """
    Process multi-labels by creating a DataFrame with each label combination as a column
    and instances marked as 1 if they belong to that combination, else 0.

    Parameters:
    y_labels (DataFrame or Series): DataFrame or Series containing multi-labels.
    y_labels_lp (Series): Series containing the processed label combinations.

    Returns:
    pd.DataFrame: DataFrame with processed labels.
    """
    # Create an empty DataFrame to store the processed labels
    y_processed = pd.DataFrame(index=y_labels.index)

    # Iterate through each label combination
    for classes in y_labels_lp.unique():
        # Check if the column for the label combination exists, if not, create a new column
        if classes not in y_processed.columns:
            y_processed[classes] = 0

        # Mark instances belonging to the label combination as 1
        y_processed.loc[y_labels_lp == classes, classes] = 1

    # Ensure all columns for label combinations are created and marked as 0 if not present
    for column in y_processed.columns:
        if column not in y_labels_lp.unique():
            y_processed[column] = 0

    # Ensure the order of columns is the same as in the original label combinations
    y_processed = y_processed[y_labels_lp.unique()]

    return y_processed
