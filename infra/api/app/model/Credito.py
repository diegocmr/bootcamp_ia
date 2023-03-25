from model.Connection import Connection 
import sys
class Credito:

    def __init__(self,login) -> None:
        self.login = login
        return None
    def getSolicitacaoAnalise(self):
        cnx = Connection()    

        sql = """
            SELECT 
                Emprestimo.id,
                dataAprovadoEmComite, 
                dataAprovadoNivelAnalista,
                status,
                valorAprovado,
                valorSolicitado,
                mensagem
            FROM Emprestimo 
            LEFT JOIN Emprestimo_Mensagem
                ON Emprestimo_Mensagem.id_emprestimo = Emprestimo.id
            WHERE 
                id_cliente = %s 
                AND status in(%s,%s,%s,%s)
        """

        cnx.execute(sql,[self.login.userSession,"emAnalise","ConfirmacaoCliente","AnalistaManual","Aprovado"])   
        return cnx.fetchone()
    def cancelarSolicitacao(self,dados):
        cnx = Connection()      
        sql = """        
            DELETE FROM Emprestimo_Mensagem WHERE id_emprestimo = %s
        """
        cnx.execute(sql,[
            dados["id_emprestimo"],           
        ])
        sql = """        
            DELETE FROM Emprestimo WHERE id = %s
        """
        cnx.execute(sql,[
            dados["id_emprestimo"],           
        ])
        cnx.commit()
        return cnx.rowcount()
    def alterarStatus (self,dados):
        
        if dados['status'] in ['Aprovado','AnalistaManual']:
            status = dados['status']
        else:
            raise Exception("Status Inválido")
        cnx = Connection()   
        sql = """        
            UPDATE Emprestimo set status = %s WHERE id = %s
        """
        cnx.execute(sql,[
            status,
            dados["id_emprestimo"]          
        ])
        cnx.commit()
        return cnx.rowcount()

    def cadastroSolicitacao(self,dados):
     
        valorSolicitado = int(dados["valorSolicitado"])
            
        if valorSolicitado < 500:
            raise Exception("Não aceitamos valores abaixo de R$ 500")

        if self.getSolicitacaoAnalise():
            raise Exception("Você já tem uma solicitação de credito em analise")

        cnx = Connection()      
        sql = """        
            INSERT INTO Emprestimo (
                valorSolicitado,
                status,
                id_cliente          
            )
            VALUES
            (
                %s,
                %s,
                %s            
            )
        """
        cnx.execute(sql,[
            valorSolicitado,
            "emAnalise",
            self.login.userSession   
        ])
        
        id_emprestimo = cnx.lastrowid()
        print(id_emprestimo, file=sys.stderr)
        if not dados["mensagem"] == "":
            sql = """        
                INSERT INTO Emprestimo_Mensagem (
                    id_emprestimo,
                    mensagem                      
                )
                VALUES
                (
                    %s,
                    %s                     
                )
            """

            cnx.execute(sql,[
                id_emprestimo,
                dados["mensagem"]             
            ])
       
        cnx.commit()
        return bool(cnx.rowcount())