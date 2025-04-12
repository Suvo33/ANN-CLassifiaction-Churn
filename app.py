import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pandas as pd 
import pickle


model=tf.keras.models.load_model('model.h5')

with open('scaler.pkl','rb') as f:
    scaler=pickle.load(f)
with open('label_encoder_gender.pkl','rb') as f:
    label_encoder_gender=pickle.load(f)
with open('onehot_encoder_geo.pkl','rb') as f:
    onehot_encoder_geo=pickle.load(f)

# Stream Lit

st.title('Customer Churn Prediction')

## User Input
geography=st.selectbox('Geography',onehot_encoder_geo.categories_[0])
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider('Age',18,90)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number of Products',1,4)
has_cr_card=st.selectbox('Has Credit Card',['Yes','No'])
is_active_member=st.selectbox('Is Active Member',['Yes','No'])

input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [1 if has_cr_card == 'Yes' else 0],
    'IsActiveMember': [1 if is_active_member == 'Yes' else 0],
    'EstimatedSalary': [estimated_salary]
})



geo_encoded=onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

input_data_scaled=scaler.transform(input_data)

prediction = model.predict(input_data_scaled)
prediction_prob= prediction[0][0]

st.write(f'Churn probability : {prediction_prob:.2f}')

if prediction_prob>0.5:
    st.write('Customer is likely to churn')
else:
    st.write('Customer is not likely to churn')



