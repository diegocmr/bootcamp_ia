$(document).ready(function(){
    
    dataTableEmprestimos = $('#emprestimos').DataTable({
        language: PTBR,
        ajax: {
            url: 'http://127.0.0.1:8080/emprestimos',
            type: 'POST',
            xhrFields: {
                withCredentials: true
            }
        },       
        columns: [
            
            { title: 'Valor Solicitado',data: 'valorSolicitado' },
            { title: 'Valor Aprovado',data: 'valorAprovado' },
            { type: "date-eu" ,title: 'Data', render:function(data, type, row){
                if (row["dataAprovadoNivelAnalista"] == "" || row["dataAprovadoNivelAnalista"] == null ) {
                    return "";
                }                 
                return formatDate(row["dataAprovadoNivelAnalista"])               
            }},
            { title: 'Status',data: 'status', render:function(data){
                return '<span class="badge badge-success rounded-pill d-inline">'+data+'</span>';
            }}
        ],
        order:[[3, 'desc']]
           
    });
    
    var funcSucess = function(data) {
        setMessage("Enviamos com sucesso sua solicitação!",".container-error",5000,"bg-success");  
        dataTableEmprestimos.ajax.reload();
    };
    var funcError = function(data) {
        setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
    };

    var data = {
        valorSolicitado,
        mensagem
    } 
    post_api("cadastro_credito", data, funcSucess, funcError)



    $('.enviar_solicitacao_credito').click(function(){
        var valorSolicitado = tratarFloat($("#valor_credito").val())
        var mensagem = $("#mensagem_credito").val()
        var credito_concorda_termos = + $("#credito_concorda_termos").is(":checked")
        if(valor_credito < 500) {
            setMessage("O valor da solicitação tem que ser maior que R$ 500",".container-error");
            return false;
        }

        if(credito_concorda_termos == 0) {
            setMessage("Você deve concordar com os termos!",".container-error");
            return false;
        }        

        var funcSucess = function(data) {
            setMessage("Enviamos com sucesso sua solicitação!",".container-error",5000,"bg-success");  
            dataTableEmprestimos.ajax.reload();
        };
        var funcError = function(data) {
            setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
        };

        var data = {
            valorSolicitado,
            mensagem
        } 
        
        post_api("cadastro_credito", data, funcSucess, funcError)

    });
    

});
