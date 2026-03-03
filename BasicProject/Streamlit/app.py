import streamlit as st 
import pandas as pd 
import numpy as np 
st.title("Hello World")
st.write("This is a sample page")
data= pd.DataFrame({
    'first_column':[1,2,3,4],
    'second_column':[20,20,13,13]
})
st.write("The dataframe")
st.write(data)

st.write("Line chart")
chart_data=pd.DataFrame(np.random.randn(20,3),columns=['a','b','c'])

st.line_chart(chart_data)