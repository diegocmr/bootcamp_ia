from model.Connection import Connection 
import sys
class Cliente:

    def __init__(self,login) -> None:
        self.login = login
        return None
    def getEmprestimos(self):
        cnx = Connection()
        print(self.login.userSession, file=sys.stderr)
        cnx.execute("SELECT * FROM Emprestimo where id_cliente = %s",[self.login.userSession])
        emprestimos = []
        emprestimo = True
        for emprestimo in cnx.fetch():
            emprestimos.append(emprestimo)

        return emprestimos
