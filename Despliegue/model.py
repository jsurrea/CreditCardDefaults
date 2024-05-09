import numpy as np
import tensorflow as tf
import pickle as pkl

model = tf.keras.models.load_model('modelo_reducido.keras')
scaler = pkl.load(open('scaler_reducido.pkl', 'rb'))

def predict(
    sex,
    age,
    education,
    marital_status,
    credit_limit,
    bill_amount,
    pay_amount,
    april,
    may,
    june,
    july,
    august,
    september,
):
    input_data = transform_input(
        sex,
        age,
        education,
        marital_status,
        credit_limit,
        bill_amount,
        pay_amount,
        april,
        may,
        june,
        july,
        august,
        september, 
    )

    input_data_processed = scaler.transform(input_data)
    return model.predict([input_data_processed[:, :6], input_data_processed[:, 6:9], input_data_processed[:, 9:]]).flatten()[0]

def transform_input(
    sex,
    age,
    education,
    marital_status,
    credit_limit,
    bill_amount,
    pay_amount,
    april,
    may,
    june,
    july,
    august,
    september,
):
    return np.array([
        int(april),
        int(may),
        int(june),
        int(july),
        int(august),
        int(september),
        credit_limit,
        bill_amount,
        pay_amount,
        sex,
        education == 'Graduate School',
        education == 'High School',
        education == 'Others',
        education == 'University',
        marital_status == 'Married',
        marital_status == 'Others',
        marital_status == 'Single',
        age == 'Young Adult (20-27)',
        age == 'Adult (28-35)',
        age == 'Middle Aged (36-45)',
        age == 'Senior (46-80)',
    ], dtype=int).reshape(1, -1)
