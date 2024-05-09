import pandas as pd

df = pd.read_excel('./default of credit card clients.xls', header=1, index_col=0)

df['SEX'] = df['SEX'].map({ 
    1: 'Male', 
    2: 'Female', 
}).astype('category')
df['SEX'] = df['SEX'].cat.reorder_categories(['Male', 'Female'], ordered=True)


df['EDUCATION'] = df['EDUCATION'].map({
    1: 'Graduate School',
    2: 'University',
    3: 'High School',
    4: 'Others',
}).astype('category')
df['EDUCATION'] = df['EDUCATION'].fillna('Others')
df['EDUCATION'] = df['EDUCATION'].cat.reorder_categories(['Graduate School', 'University', 'High School', 'Others'], ordered=True)

df['MARRIAGE'] = df['MARRIAGE'].map({
    1: 'Married',
    2: 'Single',
    3: 'Others',
}).astype('category')
df['MARRIAGE'] = df['MARRIAGE'].fillna('Others')
df['MARRIAGE'] = df['MARRIAGE'].cat.reorder_categories(['Married', 'Single', 'Others'], ordered=True)

df['AGE'] = pd.cut(
    df['AGE'], 
    bins=[20, 28, 35, 46, 80],
    labels=['Young Adult (20-27)', 'Adult (28-35)', 'Middle Aged (36-45)', 'Senior (46-80)'],
    include_lowest=True,
    ordered=True
)

for pay_column in df.columns[5:11]:
    df[pay_column] = df[pay_column].map({ -1: 0, 0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1 })
    df[pay_column] = df[pay_column].fillna(0).astype(int)

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
    'BILL_AMT1': 'Bill Amount in September',
    'BILL_AMT2': 'Bill Amount in August',
    'BILL_AMT3': 'Bill Amount in July',
    'BILL_AMT4': 'Bill Amount in June',
    'BILL_AMT5': 'Bill Amount in May',
    'BILL_AMT6': 'Bill Amount in April',
    'PAY_AMT1': 'Amount Paid in September',
    'PAY_AMT2': 'Amount Paid in August',
    'PAY_AMT3': 'Amount Paid in July',
    'PAY_AMT4': 'Amount Paid in June',
    'PAY_AMT5': 'Amount Paid in May',
    'PAY_AMT6': 'Amount Paid in April',
    'default payment next month': 'Defaulted Payment Next Month',
})

df.to_csv('data_visualizaciones.csv')
