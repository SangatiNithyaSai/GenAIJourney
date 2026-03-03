import pandas as pd
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle

model=load_model(model.h5)

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)

with open('onehot_encoder_gender.pkl','rb') as file:
    onehot_encoder_gender=pickle.load(file)

st.title("Churn predictor")
name=st.text_input("Enter the name")
age=st.slider("Select the age",10,30)