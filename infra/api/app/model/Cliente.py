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
