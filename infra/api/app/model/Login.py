from model.Connection import Connection 
import secrets
import sys
import datetime

userSession = False

class Login:
    def __init__(self) -> None:
        return None;
    def efetuarLogin(self,login,senha) -> bool:
        cnx = Connection()
        #print((login,senha), file=sys.stderr)
        cnx.execute("SELECT id FROM Cliente where cnpj = %s AND senha = %s",(login,senha))
        user = cnx.fetchone()
       
        if(user):
            self.criarSessao(user[0])

        return  True if user else False
    def criarSessao(self,id_cliente):
        cnx = Connection()
        self.token = ""
        token = secrets.token_urlsafe()
        cnx.execute(
            "INSERT External_Token (id_cliente,token,dataCriacao,dataExpiracao) values (%s,%s,%s,%s)",
            (id_cliente,token,datetime.date.today(),datetime.date.today() + datetime.timedelta(days=30)))
        if(cnx.rowcount()):
            cnx.commit()
            self.token = token
            return True
        else:
            return False 
    def getToken(self):
        return self.token
    def efetuarLoginToken(self,token): 
        global userSession
        print(token, file=sys.stderr)
        if not token:
            raise Exception("O token informado está inválido")
        cnx = Connection()
        sql = """
            SELECT 
                External_Token.id_cliente
            FROM External_Token                
            WHERE
                External_Token.token = %s
        """

        cnx.execute(sql,(token))
        user = cnx.fetchone()
        if (user):
            userSession = user[0]
        else:
            raise Exception("O token informado está inválido")
    