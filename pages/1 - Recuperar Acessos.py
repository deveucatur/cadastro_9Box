import streamlit as st
from PIL import Image
import pymysql
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="Recuperar Acesso",
    page_icon=Image.open('icon.png'),
    layout="centered",
)

conexao = pymysql.connect(
    passwd='npmyY8%UZ041',
    port=3306,
    user='ninebox',
    host='192.168.10.71',
    database='Colaboradores'
)

mycursor = conexao.cursor()
comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()

listEmails = [x[7] for x in dadosUser]
st.image(Image.open("logo.png"), width = 250)

with st.form('Esqueceu a senha'):
    st.subheader('Recupere seu acesso ao 9Box!')
    cod_cadastr = st.text_input('Insira o código de cadastro')
    matricul = st.text_input('Matricula')
    new_email = st.text_input('Novo e-mail/login')
    new_senha = st.text_input('Nova senha', type='password')

    btao = st.form_submit_button('Alterar dados')

    if btao:
        new_senha_hashe = stauth.Hasher([str(new_senha).strip()]).generate()[0]
        if new_email not in listEmails:
            maiusculo = False

            for string_email in new_email:
                if string_email.isupper():
                    maiusculo = True

            if maiusculo == False:
                linrow = [str(new_email).strip(), str(new_senha).strip(), new_senha_hashe]
                colunas = ['Email', 'senha', 'Senha_hashe']
                    
                for i in range(len(colunas)):
                    sql = f"UPDATE Usuarios SET {colunas[i]} = '{linrow[i]}' WHERE (cod_acesso = '{cod_cadastr}') AND (Matricula = {matricul});"
                    mycursor.execute(sql)
                    conexao.commit()

                st.info('''Dados de login alterados com sucesso
                    
Basta fazer o [login](https://9box.eucatur.com.br/) na tela principal do sistema 9Box.''') 
            else:
                st.error("O e-mail só pode conter letras minúsculas.")
        else:
            st.error("E-mail já utilizado por outro usuário.")
            
