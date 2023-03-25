$(document).ready(function(){
    $(".container-solicitar_emprestimo_resumo").hide();
    $(".container-solicitar_emprestimo").hide();
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
            
            { title: 'Valor Solicitado',data: 'valorSolicitado',render:function(data, type, row){
                if (data == "" || data == null ) {
                    return "";
                }                 
                return "R$ "+ data;           
            }},
            { title: 'Valor Aprovado',data: 'valorAprovado',render:function(data, type, row){
                if (data == "" || data == null ) {
                    return "";
                }                 
                return "R$ "+ data;           
            }},
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
        order:[[2, 'desc']]
           
    });
    $(".aceitar_credito").click(function(){
        var id_emprestimo = $("#id_solitacao_credito").val()
        var funcSucess = function () {
            $("#tab-solicitar").click()
        }
        var funcError = function(data) {
            setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
        };
        post_api("update_credito_status", {status:"Aprovado",id_emprestimo}, funcSucess, funcError)
    });
    $(".enviar_analista_credito").click(function(){
        var id_emprestimo = $("#id_solitacao_credito").val()
        var funcSucess = function () {
            $("#tab-solicitar").click();
        }
        var funcError = function(data) {
            setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
        };
        post_api("update_credito_status", {status:"AnalistaManual",id_emprestimo}, funcSucess, funcError)
    });
    $(".cancelar_credito").click(function(){
        var id_emprestimo = $("#id_solitacao_credito").val()
        var funcSucess = function () {
            $("#tab-solicitar").click();
        }
        var funcError = function(data) {
            setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
        };
        post_api("cancelar_credito", {id_emprestimo}, funcSucess, funcError)
    });
    $("#tab-solicitar").click(function(){
        dataTableEmprestimos.ajax.reload();
        var funcSucess = function(data) {
            var credito = data["credito"];
            if(credito) {    
                $(".texto_aviso_credito").hide();     
                $(".container-solicitar_emprestimo_resumo").show();
                $(".valor_resumo_container").show();
                $(".container-solicitar_emprestimo").hide();            
                $("#valor_credito_resumo").val("R$ " + credito["valorSolicitado"]);
                $("#credito_status_resumo").val(credito["status"]);
                $("#id_solitacao_credito").val(credito["id"]);
                $(".container_botao_credito_aceitar").hide();
                $(".valor_aprovado_resumo").hide();                
                $("#mensagem_credito_resumo").html(credito["mensagem"]);

                if(credito["status"] == "ConfirmacaoCliente" || credito["status"] == "Aprovado" || credito["status"] == "AnalistaManual"){
                    $(".valor_aprovado_resumo").show();
                    $("#valor_credito_aprovado_resumo").val("R$ " + tratarFloat(credito["valorAprovado"]).toFixed(2));  
                    if(credito["status"] != "Aprovado" && credito["status"] != "AnalistaManual"){
                        $(".container_botao_credito_aceitar").show();
                        if(tratarFloat(credito["valorAprovado"]) < 50){
                            $(".aceitar_credito ").hide();
                        }else{
                            $(".aceitar_credito ").show();
                        }
                    }else{          
                        if (credito["status"] == "Aprovado") {
                            $(".valor_resumo_container").hide();
                            $(".valor_aprovado_resumo").show();
                        } else{
                            $(".valor_resumo_container").show();
                            $(".valor_aprovado_resumo").hide();
                            $(".texto_aviso_credito").show();  
                            $(".texto_aviso_credito").html("<b>Aguarde até que um dos nossos analistas aprove sua solicitação<b>");  
                        }        
                        
                        $(".container_botao_credito_aceitar").hide();
                    }  
                }

                return true;
            }else{
                $(".container-solicitar_emprestimo_resumo").hide();
                $(".container-solicitar_emprestimo").show();   
            }
        };
        var funcError = function(data) {
            setMessage("Ocorreu um erro, Tente novamente mais tarde",".container-error");  
        };
    
        post_api("get_credito_analise", {}, funcSucess, funcError)
    });
    
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
            $("#tab-solicitar").click();
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
