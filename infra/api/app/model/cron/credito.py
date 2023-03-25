import pandas as pd
import pickle
import json
import numpy as np
import warnings
import sys, os
import time
from model.Connection import Connection
warnings.filterwarnings("ignore") 

def model_loader(prazoMedioRecebimentoVendas,
                    titulosEmAberto,
                    valorSolicitado,
                    totalAtivo,
                    faturamentoBruto,
                    periodoDemonstrativoEmMeses,
                    intervaloFundacao,
                    capitalSocial,
                    empresa_MeEppMei,
                    primeiraCompra_Y,
                    primeiraCompra_m,
                    periodoBalanco_Y,
                    periodoBalanco_m,
                    qtd_solic):
    df = pd.DataFrame([[prazoMedioRecebimentoVendas,
                        titulosEmAberto,
                        valorSolicitado,
                        totalAtivo,
                        faturamentoBruto,
                        periodoDemonstrativoEmMeses,
                        intervaloFundacao,
                        capitalSocial,
                        empresa_MeEppMei,
                        primeiraCompra_Y,
                        primeiraCompra_m,
                        periodoBalanco_Y,
                        periodoBalanco_m,
                        qtd_solic]])
    df.columns = ['prazoMedioRecebimentoVendas',
                  'titulosEmAberto',
                  'valorSolicitado',
                  'totalAtivo',
                  'faturamentoBruto',
                  'periodoDemonstrativoEmMeses',
                  'intervaloFundacao',
                  'capitalSocial',
                  'empresa_MeEppMei',
                  'primeiraCompra_Y',
                  'primeiraCompra_m',
                  'periodoBalanco_Y',
                  'periodoBalanco_m',
                  'qtd_solic']
    
    todasColunas = ['prazoMedioRecebimentoVendas', 'titulosEmAberto', 'valorSolicitado',
                        'totalAtivo', 'faturamentoBruto', 'periodoDemonstrativoEmMeses',
                        'intervaloFundacao', 'capitalSocial', 'empresa_MeEppMei',
                        'valorAprovado', 'primeiraCompra_Y', 'primeiraCompra_m',
                        'periodoBalanco_Y', 'periodoBalanco_m', 'qtd_solic']

    with open ('/Models/label_encoder_10col.json', 'r') as jsonfile:
        dict_label_encode_10col = json.load(jsonfile)
    
    with open ('/Models/label_encoder_16col.json', 'r') as jsonfile:
        dict_label_encode_16col = json.load(jsonfile)

    with open ('/Models/gm_clusterizer.pkl', 'rb') as picklefile:
        gm_clusterizer = pickle.load(picklefile)
        ### obtendo cluster
        
    df_empresa = df.drop(columns = ['primeiraCompra_Y','primeiraCompra_m','periodoBalanco_Y','periodoBalanco_m','valorSolicitado'])
    for col in dict_label_encode_10col:
        df_empresa[col] = df_empresa[col].apply(lambda x: dict_label_encode_10col[col][x] for x in df_empresa[col])
    cluster = gm_clusterizer.predict(df_empresa)[0]
    print ('cluster predito:',cluster)
    
    ### label encoding do df
    for col in dict_label_encode_16col:
        df[col] = df[col].apply(lambda x: dict_label_encode_16col[col][x] for x in df_empresa[col])

    ### rodando standard scaler
    # mockando valorAprovado
    df['valorAprovado'] = np.nan
    df = df[['prazoMedioRecebimentoVendas', 'titulosEmAberto', 'valorSolicitado',
       'totalAtivo', 'faturamentoBruto', 'periodoDemonstrativoEmMeses',
       'intervaloFundacao', 'capitalSocial', 'empresa_MeEppMei',
       'valorAprovado', 'primeiraCompra_Y', 'primeiraCompra_m',
       'periodoBalanco_Y', 'periodoBalanco_m', 'qtd_solic']] #retornando ordem das colunas
    
    with open('/Models/standard_scaler_15cols_cluster{}.pkl'.format(cluster), 'rb') as picklefile:
        sc = pickle.load(picklefile)
        df = sc.transform(df)
        df = pd.DataFrame(df)
        df.columns = todasColunas
    ### aplicando modelo
    with open('/Models/rf_cluster{}.pkl'.format(cluster), 'rb') as picklefile:
        rf = pickle.load(picklefile)
    df.drop(columns = ['valorAprovado'], inplace=True)
    predict = rf.predict(df)[0]
    df['valorAprovado'] = predict # inserindo predito no dataframe
    df = sc.inverse_transform(df) # escalando para valores reais
    df = pd.DataFrame(df) #gerando dataframe
    df.columns = todasColunas #gerando colunas
    valorAprovado = float(df['valorAprovado']) #obtendo valorAprovado
    print ('valorAprovado',valorAprovado)
    return valorAprovado

def rodarCron():   
    cnx = Connection()
    sql = """

    SELECT 
        Emprestimo.id,
        Cliente.prazoMedioRecebimentoVendas,
        Cliente.titulosEmAberto,
        Emprestimo.valorSolicitado,
        Cliente.totalAtivo,
        Cliente.faturamentoBruto,
        Cliente.periodoDemonstrativoEmMeses,
        (
            CASE 
                WHEN (Cliente.anoFundacao is null) THEN 'De 0 a 5 anos'
                WHEN (Cliente.anoFundacao = 0) THEN 'De 0 a 5 anos'
                WHEN ((YEAR(CURDATE()) - Cliente.anoFundacao) > 0 and (YEAR(CURDATE()) - Cliente.anoFundacao) < 6) THEN 'De 0 a 5 anos'
                WHEN ((YEAR(CURDATE()) - Cliente.anoFundacao) > 5 and (YEAR(CURDATE()) - Cliente.anoFundacao) < 11) THEN 'De 6 a 10 anos'
                WHEN ((YEAR(CURDATE()) - Cliente.anoFundacao) > 10 and (YEAR(CURDATE()) - Cliente.anoFundacao) < 17) THEN 'De 11 a 16 anos'
                ELSE "Acima de 17 anos"
            END
        ) as intervaloFundacao,
        Cliente.capitalSocial,
        Cliente.empresa_MeEppMei,
        YEAR(Cliente.primeira_compra) as primeiraCompra_Y,
        MONTH(Cliente.primeira_compra) as primeiraCompra_m,
        YEAR(Cliente.periodoBalanco) as periodoBalanco_Y,
        MONTH(Cliente.periodoBalanco) as periodoBalanco_m,
        (
            SELECT count(*) FROM Emprestimo as Emprestimo_Count where Emprestimo_Count.id_cliente = Cliente.id AND NOT status = %s 
        ) as qtd_solic

    FROM Emprestimo
    INNER JOIN Cliente
        ON Cliente.id = Emprestimo.id_cliente
    WHERE   
        Emprestimo.status = %s

    """
    cnx.execute(sql,['emAnalise','emAnalise'])

    def tratarNone(data):
        if data is None:
            return 0
        return data

    cnx_credito = Connection()
    for credito in cnx.fetch():
        valor_credito = model_loader(
            float(tratarNone(credito["prazoMedioRecebimentoVendas"])),
            float(tratarNone(credito["titulosEmAberto"])),
            float(tratarNone(credito["valorSolicitado"])),
            float(tratarNone(credito["totalAtivo"])),
            float(tratarNone(credito["faturamentoBruto"])),
            float(tratarNone(credito["periodoDemonstrativoEmMeses"])),
            credito["intervaloFundacao"],
            float(credito["capitalSocial"]),
            bool(tratarNone(credito["empresa_MeEppMei"])),
            float(tratarNone(credito["primeiraCompra_Y"])),
            float(tratarNone(credito["primeiraCompra_m"])),
            float(tratarNone(credito["periodoBalanco_Y"])),
            float(tratarNone(credito["periodoBalanco_m"])),
            float(tratarNone(credito["qtd_solic"]))
        )
        valor_credito = float(format(valor_credito, '.2f'))

        if valor_credito < 0:
            valor_credito = 0
        if valor_credito >= credito["valorSolicitado"]:
            cnx_credito.execute("UPDATE Emprestimo set status = %s, valorAprovado = %s, dataAprovadoNivelAnalista = CURDATE() WHERE id = %s",["Aprovado",credito["valorSolicitado"],credito["id"]])
            cnx_credito.commit()
        if valor_credito < credito["valorSolicitado"]:
            cnx_credito.execute("UPDATE Emprestimo set status = %s, valorAprovado = %s, dataAprovadoNivelAnalista = CURDATE() WHERE id = %s",["ConfirmacaoCliente",valor_credito,credito["id"]])
            cnx_credito.commit()
        print(valor_credito, file=sys.stderr) 
        print(credito, file=sys.stderr)
    cnx.close()
    cnx_credito.close()
