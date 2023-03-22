from model.Connection import Connection 
import sys
class Cliente:

    def __init__(self,login) -> None:
        self.login = login
        return None
    def getEmprestimos(self):
        cnx = Connection()      
        cnx.execute("SELECT * FROM Emprestimo where id_cliente = %s",[self.login.userSession])
        emprestimos = []
        emprestimo = True
        cont = 1
        for emprestimo in cnx.fetch():
            emprestimos.append(emprestimo)
            cont = cont+ 1
            if cont > 10:
                break
        return emprestimos
    def cadastroCliente(self,dados):
        cnx = Connection()      
        sql = """
        
        INSERT INTO Cliente (
            cnpj,
            razaoSocial,
            nomeFantasia,
            capitalSocial,
            totalAtivo,
            totalPatrimonioLiquido,
            faturamentoBruto,
            senha,
            empresa_MeEppMei
        )
        VALUES
        (
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
        cnx.execute(sql,[
            dados["cnpj"],
            dados["razaoSocial"],
            dados["nomeFantasia"],
            dados["capitalSocial"],
            dados["totalAtivo"],
            dados["totalPatrimonioLiquido"],
            dados["fataturamentoBruto"],
            dados["senha"],
            dados["empresa_MeEppMei"]
        ])
        cnx.commit()
        return bool(cnx.rowcount())