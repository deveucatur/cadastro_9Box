#ESSE AQUI SE REFERE AO CÓDIGO DO CADASTRO QUE ESTÁ SOZINHO

import streamlit as st
import pymysql
from PIL import Image
import streamlit_authenticator as stauth


conexao = pymysql.connect(
    passwd='npmyY8%UZ041',
    port=3306,
    user='ninebox',
    host='192.168.0.7',
    database='Colaboradores'
)

mycursor = conexao.cursor()

st.set_page_config(
page_title="9box | Novo Cadastro",
page_icon=Image.open('icon.png'),
layout="centered")

image = Image.open(('logo.png'))
st.image(image, width = 250)
comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
listCod = mycursor.fetchall()


def CadastroDeUsuarios():
    with st.form("Formulário de Cadastro"):
        st.subheader("Cadastro de Novos Usuários | 9box")
        codCadas = st.text_input("Insira o código de cadastro de novo usuário recebido")
        unidade = st.selectbox("Unidade de Negócio",  ["CEEM Ariquemes",
                                                          "CEEM Boa Vista - Manaus",
                                                          "CEEM Cacoal",
                                                          "CEEM Campinas",
                                                          "CEEM Campo Grande",
                                                          "CEEM Cascavel",
                                                          "CEEM Cuiaba",
                                                          "CEEM Curitiba",
                                                          "CEEM Goiânia",
                                                          "CEEM Jí-Parana",
                                                          "CEEM Porto Alegre",
                                                          "CEEM Porto Velho",
                                                          "CEEM Pres. Prudente",
                                                          "CEEM Rio Branco",
                                                          "CEEM Rondonópolis",
                                                          "CEEM São Paulo",
                                                          "CEEM Vilhena",
                                                          "Corporativo Cascavel",
                                                          "Corporativo Jí-Parana"])
        col1, col2 = st.columns((2,0.8))
        with col1:
            nome = st.text_input("Nome")

        with col2:
            matricul = st.text_input('Matricula')
        

        email = st.text_input("Insira seu e-mail/Login")
        col1, col2 = st.columns(2)
        with col1:
            senhaaux =st.text_input("Insira uma senha", type = "password")
        with col2:
            senha = st.text_input("Confirme a senha", type = "password")
            if senha != senhaaux:
                st.error("As senhas precisam ser iguais")
        
        
        submitted = st.form_submit_button("Cadastrar")
        if submitted and senha == senhaaux:
            if codCadas in [x[1] for x in listCod]:
                linhaBD = [x for x in range(len(listCod)) if  str(listCod[x][1]) == codCadas ][0]

                maiusculo = False

                for string_email in email:
                    if string_email.isupper():
                        maiusculo = True

                if maiusculo == False:
                    if listCod[linhaBD][7] == '' or listCod[linhaBD][7] == None and email not in [x[7] for x in listCod] and matricul not in [x[4] for x in listCod]:
                        #f"{nome,email,senha,stauth.Hasher(senha).generate()[0],1}"
                        linrow = [unidade, matricul, nome, str(email).strip(), str(senha).strip(), stauth.Hasher([senha]).generate()[0]]
                        colunas = ['Unid_Negocio', 'Matricula', 'Nome',
                                        'Email', "senha", 'Senha_hashe']
                        
                        for i in range(len(linrow)):   
                            sql = f"UPDATE Usuarios SET {colunas[i]} = '{linrow[i]}' WHERE cod_acesso = '{codCadas}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        
                        st.success("Cadastro Realizado com Sucesso!")
                        st.success("""Realize seu Login

Com seu email e sua senha realize o login no seguinte link:

---
https://9box.eucatur.com.br/
---""")

                    else:
                        st.error("Código de cadastro ou e-mail já foi utilizado")
                else:
                    st.error("O e-mail só pode conter letras minúsculas")
            else:
                st.error("Código de cadastro inválido")


st.write("---")
CadastroDeUsuarios()
