import streamlit as st
import pandas as pd
name=st.text_input("Enter the name")

age=st.slider("Select the age",18,54,22)
st.write(f"Age is {age}")
options=["Java","Python","C++"]
choice=st.selectbox("choose your Programming language",options)

if name:
    st.write("Hello Name",name)


data={
    "name":["Raju","Kiran","Murali"],
    "age":[19,20,29]
}
df=pd.DataFrame(data)
st.write(df)

uploaded_file=st.file_uploader("Upload the file",type=csv)

if uploaded_file:
    final_data=pd.read_csv(uploaded_file)
    st.write(final_data)