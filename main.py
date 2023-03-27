import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
from PIL import Image
import random
import string

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()

st.set_page_config(
page_title="9box | Novo Cadastro",
page_icon=Image.open('icon.png'),
layout="centered")

image = Image.open(('logo.png'))
st.image(image, width = 250)
#comando1 = 'ALTER TABLE Usuarios MODIFY senha VARCHAR(30) NOT NULL;'
#mycursor.execute(comando1)
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
        nome = st.text_input("Nome")
        col1, col2 = st.columns(2)
        with col1:
            funcao = st.selectbox('Função', ["Líder de Processos", "Dono de processo", "Gestor de Processos",
                                             "Executor de Processos"])
        with col2:
            matricul = st.text_input('Matricula')
        
        if funcao == "Dono de processo":
            macroproc = st.selectbox('Macroprocesso', ["Relacionamento com Cliente - Pessoas",
                                                           "Relacionamento com Cliente - Cargas",
                                                           "Administrar",
                                                           "Operar",
                                                           "Formulação Estratégica"])

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
            print("teste3")
            if codCadas in [x[1] for x in listCod]:
                linhaBD = [x for x in range(len(listCod)) if  str(listCod[x][1]) == codCadas ][0]
                if listCod[linhaBD][7] == '' or listCod[linhaBD][7] == None and email not in [x[6] for x in listCod] and matricul not in [x[3] for x in listCod]:
                    #f"{nome,email,senha,stauth.Hasher(senha).generate()[0],1}"
                    if funcao != 'Dono de processo':
                        linrow = [unidade, matricul, nome, funcao, email, senha ]
                        colunas = ['Unid_Negocio', 'Matricula', 'Nome',
                                    'Cargo','Email', "senha"]
                    else:
                        linrow = [unidade, matricul, nome, funcao, email, senha ]
                        colunas = ['Unid_Negocio', 'Matricula', 'Nome',
                                    'Cargo','Email', "senha"]

                    for i in range(len(linrow)):   
                            #sql = f'INSERT INTO Usuario({colunas[0]},{colunas[1]},{colunas[2]},{colunas[3]},{colunas[4]},{colunas[5]},{colunas[6]}) VALUES ("{gerar_sequencia_aleatoria}", )'
                        sql = f"UPDATE Usuarios SET {colunas[i]} = '{linrow[i]}' WHERE cod_acesso = '{codCadas}'"
                        mycursor.execute(sql)
                        conexao.commit()
                    
                    st.success("Cadastro Realizado com Sucesso!")
                    st.success("Realize seu Login")

                else:
                    st.error("Código de cadastro ou e-mail já foi utilizado")
            else:
                st.error("Código de cadastro inválido")


st.write("---")
CadastroDeUsuarios()