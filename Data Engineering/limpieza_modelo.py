import pandas as pd
import numpy as np

df = pd.read_excel('./default of credit card clients.xls', header=1, index_col=0)

df['SEX'] = df['SEX'].map({ 1: 1, 2: 0 })  # 1: Male, 0: Female 
df['EDUCATION'] = df['EDUCATION'].map({ 1: 'Graduate School', 2: 'University', 3: 'High School', 4: 'Others' }).fillna('Others').astype('category')
df['MARRIAGE'] = df['MARRIAGE'].map({ 1: 'Married', 2: 'Single', 3: 'Others' }).fillna('Others').astype('category')
df['AGE'] = pd.cut(
    df['AGE'], 
    bins=[20, 28, 35, 46, 80],
    labels=['Young Adult (20-27)', 'Adult (28-35)', 'Middle Aged (36-45)', 'Senior (46-80)'],
    include_lowest=True,
    ordered=True
)
for pay_column in [f'PAY_{i}' for i in [0,2,3,4,5,6]]:
    df[pay_column] = df[pay_column].map({ -1: 0, 0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1 }).fillna(0).astype(int)

df['BILL_AMT'] = df[[f'BILL_AMT{i}' for i in range(1, 7)]].median(axis=1)
df['PAY_AMT'] = df[[f'PAY_AMT{i}' for i in range(1, 7)]].median(axis=1)
df = df.drop(columns=[f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)])

df = df.rename(columns={
    'LIMIT_BAL': 'Credit Limit',
    'SEX': 'Sex',
    'EDUCATION': 'Education',
    'MARRIAGE': 'Marriage',
    'AGE': 'Age',
    'PAY_0': 'Payed Status in September',
    'PAY_2': 'Payed Status in August',
    'PAY_3': 'Payed Status in July',
    'PAY_4': 'Payed Status in June',
    'PAY_5': 'Payed Status in May',
    'PAY_6': 'Payed Status in April',
    'BILL_AMT': 'Average Bill Amount',
    'PAY_AMT': 'Average Pay Amount',
    'default payment next month': 'Defaulted Payment',
})

df = pd.get_dummies(df, dtype=int)

pay_status_input = ['Payed Status in April', 'Payed Status in May', 'Payed Status in June', 'Payed Status in July', 'Payed Status in August', 'Payed Status in September']
credit_input = ['Credit Limit', 'Average Bill Amount', 'Average Pay Amount']
personal_input = ['Sex', 'Education_Graduate School', 'Education_High School', 'Education_Others', 'Education_University', 'Marriage_Married', 'Marriage_Others', 'Marriage_Single', 'Age_Young Adult (20-27)', 'Age_Adult (28-35)', 'Age_Middle Aged (36-45)', 'Age_Senior (46-80)']
target = ['Defaulted Payment']

df = df[pay_status_input + credit_input + personal_input + target]
df.to_csv('./datos_modelo.csv')
