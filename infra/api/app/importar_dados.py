import mysql.connector
import pandas as pd
import numpy as np
import sys
from mysql.connector import Error
try:
    cnx = mysql.connector.connect(
        user='root', 
        password='root',
        host='bancodados',
        database='mydb'
    )
except Error as e:
    print("Error while connecting to MySQL", e)

mycursor = cnx.cursor(prepared=True)
mycursor.execute('SELECT count(*) FROM Cliente ')
numDados = mycursor.fetchone()
mycursor.close()

if(numDados[0] > 0) :
    print("Os dados já foram carregados")
    sys.exit()

dataFrame = pd.read_csv("/data/dadosclientes.csv")
dataFrame = dataFrame.astype(object).replace(np.nan, None)

sql_cliente = """
    INSERT INTO Cliente (   
        prazoMedioRecebimentoVendas,         
        cnpj,
        razaoSocial,
        nomeFantasia,
        capitalSocial,
        empresa_MeEppMei,
        primeira_compra,
        totalAtivo,
        totalPatrimonioLiquido,
        faturamentoBruto,
        anoFundacao,
        periodoBalanco,
        titulosEmAberto,
        periodoDemonstrativoEmMeses
    ) VALUES (   
        %s,       
        %s,
        %s, 
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
"""   

sql_emprestimo = """
    INSERT INTO Emprestimo (
        valorSolicitado,
        valorAprovado,
        status,
        dataAprovadoEmComite,
        dataAprovadoNivelAnalista,
        id_cliente
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
"""
num_rows = len(dataFrame)
count = 0
for index, row in dataFrame.iterrows():
    
    mycursor = cnx.cursor(prepared=True)
    mycursor.execute('SELECT id FROM Cliente WHERE cnpj = %s', [(row.cnpjSemTraco)])
    cliente = mycursor.fetchone()
    mycursor.close()
    if cliente:
        id_cliente = cliente[0]
    else:
        mycursor = cnx.cursor(prepared=True)
                    
        mycursor.execute(sql_cliente, (
            row.prazoMedioRecebimentoVendas,
            row.cnpjSemTraco,
            row.razaoSocial,
            row.nomeFantasia,
            row.capitalSocial,
            row.empresa_MeEppMei,
            row.primeiraCompra,
            row.totalAtivo,
            row.totalPatrimonioLiquido,
            row.faturamentoBruto,
            row.anoFundacao,
            row.periodoBalanco,
            row.titulosEmAberto,
            row.periodoDemonstrativoEmMeses
        ))
        id_cliente = mycursor.lastrowid
        mycursor.close()

    # Inserir o emprestimo
        
    mycursor = cnx.cursor(prepared=True)
    mycursor.execute(sql_emprestimo, (
        row.valorSolicitado,
        row.valorAprovado,
        row.status,
        row.dataAprovadoEmComite,
        row.dataAprovadoNivelAnalista,
        id_cliente        
    )) 
    mycursor.close()
    count = count + 1
    if((count % 500) == 0 ):
        print("Baixando a base ",count," de ",num_rows," de registros")


cnx.commit()

