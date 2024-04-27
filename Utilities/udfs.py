#Imports
import pandas as pd
import numpy as np

# Survey data udfs
# define udf
def determine_fm_cardio(row):
    if row['f_cardio'] == 1.0 or row['m_cardio'] == 1.0:
        return 1.0
    elif row['f_cardio'] == 0.0 or row['m_cardio'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_hyper(row):
    if row['f_hyper'] == 1.0 or row['m_hyper'] == 1.0:
        return 1.0
    elif row['f_hyper'] == 0.0 or row['m_hyper'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_dys(row):
    if row['f_dys'] == 1.0 or row['m_dys'] == 1.0:
        return 1.0
    elif row['f_dys'] == 0.0 or row['m_dys'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_ap(row):
    if row['f_ap'] == 1.0 or row['m_ap'] == 1.0:
        return 1.0
    elif row['f_ap'] == 0.0 or row['m_ap'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_ami(row):
    if row['f_ami'] == 1.0 or row['m_ami'] == 1.0:
        return 1.0
    elif row['f_ami'] == 0.0 or row['m_ami'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_lipid(row):
    if row['f_lipid'] == 1.0 or row['m_lipid'] == 1.0:
        return 1.0
    elif row['f_lipid'] == 0.0 or row['m_lipid'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_hf(row):
    if row['f_hf'] == 1.0 or row['m_hf'] == 1.0:
        return 1.0
    elif row['f_hf'] == 0.0 or row['m_hf'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_dm(row):
    if row['f_dm'] == 1.0 or row['m_dm'] == 1.0:
        return 1.0
    elif row['f_dm'] == 0.0 or row['m_dm'] == 0.0:
        return 0.0
    else:
        return np.nan

def determine_fm_Thyroid(row):
    if row['f_Thyroid'] == 1.0 or row['m_Thyroid'] == 1.0:
        return 1.0
    elif row['f_Thyroid'] == 0.0 or row['m_Thyroid'] == 0.0:
        return 0.0
    else:
        return np.nan
    
# Categorize score into different levels
def categorize_rand36_score(score):
    if score >= 80:
        return 4 #'High'
    elif score >= 60:
        return 3 #'Mid-High'
    elif score >= 40:
        return 2 #'Medium'
    elif score >= 20:
        return 1 #'Mid-Low'
    elif score >= 0:
        return 0 #'Low'
    else:
        return np.nan
    
    
# HADS table
# Define a function to categorize anxiety levels
def categorize_anxiety_or_depression(score):
    if pd.isna(score):
        return np.nan  # Retain NaN values
    elif score <= 7:
        return 0 #'Normal'
    elif 8 <= score <= 10:
        return 1 #'Mild'
    elif 11 <= score <= 14:
        return 2 #'Moderate'
    else:  # score >= 15
        return 3 #'Severe'

def categorize_HAD_total(score):
    if pd.isna(score):
        return np.nan  # Retain NaN values
    elif score <= 14:
        return 0 #'Normal'
    elif 14 <= score <= 28:
        return 1 #'Moderate'
    elif 29 <= score <= 42:
        return 2 #'Severe'
    
# MNA (Mini Nutritional Assessment)
# tatal score is 30: above 24 meaning good；17-23.5 meaning moderate；below 17 meaning bad
def categorize_mna(score):
    if pd.isna(score):
        return np.nan #'NaN'
    elif score >= 24:
        return 0 #'Good Nutitional Status'
    elif score >= 17:
        return 1 #'At Risk of Malnutrition'
    else:
        return 2 #'Severe Malnutrition'



# AUDIT Alcohol Use Disorders Identification Test
def categorize_AUDIT(score):
    if pd.isna(score):
        return np.nan #'NaN'  # Retain NaN values
    elif score <= 7:
        return 0 #'safe'
    elif 8 <= score <= 15:
        return 1 #'Moderate'
    elif 16 <= score <= 19:
        return 2 #'High Risk'
    else:
        return 3 #'Severe'