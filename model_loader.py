import pandas as pd
import pickle
import json
import numpy as np
import warnings
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

    with open ('Models/label_encoder_10col.json', 'r') as jsonfile:
        dict_label_encode_10col = json.load(jsonfile)
    
    with open ('Models/label_encoder_16col.json', 'r') as jsonfile:
        dict_label_encode_16col = json.load(jsonfile)

    with open ('Models/gm_clusterizer.pkl', 'rb') as picklefile:
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
    
    with open('Models/standard_scaler_15cols_cluster{}.pkl'.format(cluster), 'rb') as picklefile:
        sc = pickle.load(picklefile)
        df = sc.transform(df)
        df = pd.DataFrame(df)
        df.columns = todasColunas
    ### aplicando modelo
    with open('Models/rf_cluster{}.pkl'.format(cluster), 'rb') as picklefile:
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




if __name__ == '__main__':
    model_loader(0,
                0.0,
                100000.0,
                1876039.0,
                1818311.0,
                12.0,
                'Acima de 17 anos',
                90000.0,
                True,
                2015.0,
                12.0,
                2019.0,
                12.0,
                2.0)