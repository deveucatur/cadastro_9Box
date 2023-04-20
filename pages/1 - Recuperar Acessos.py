import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import mysql.connector


st.set_page_config(
    page_title="Recuperar Acesso",
    page_icon=Image.open('icon.png'),
    layout="centered",
)


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()

st.image(Image.open("logo.png"), width = 250)

with st.form('Esqueceu a senha'):
        st.subheader('Recupere seu acesso ao 9Box!')
        cod_cadastr = st.text_input('Insira o código de cadastro')
        matricul = st.text_input('Matricula')
        new_email = st.text_input('Novo e-mail/login')
        new_senha = st.text_input('Nova senha')

        btao = st.form_submit_button('Alterar dados')

        if btao:
            linrow = [new_email, new_senha]
            colunas = ['Email', 'senha']
            
            for i in range(len(colunas)):
                sql = f"UPDATE Usuarios SET {colunas[i]} = '{linrow[i]}' WHERE (cod_acesso = '{cod_cadastr}') AND (Matricula = 232);"
                mycursor.execute(sql)
                conexao.commit()

            st.info('''Dados de login alterados com sucesso
            
Basta fazer o [login](https://nineboxeucatur.streamlit.app/) na tela principal do sistema 9Box.''')
            