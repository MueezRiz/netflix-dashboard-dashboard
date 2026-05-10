import streamlit as st
import plotly.express as px
fig = px.bar(x=[1,2], y=[3,4])
st.plotly_chart(fig, width='stretch')
