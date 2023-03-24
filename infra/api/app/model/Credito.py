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
                AND status = %s
        """

        cnx.execute(sql,[self.login.userSession,"emAnalise"])   
        return cnx.fetchone()
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