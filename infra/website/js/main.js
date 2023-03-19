$(document).ready(function(){
    if(document.domain == "localhost"){
        window.location.href = "http://127.0.0.1:8081/";
    }
    $(".botao_login").click(function(){
        var cnpj = $("#campo_cnpj").val();
        var senha = $("#campo_senha").val();

        if(cnpj.length < 2 || senha.length < 2){
            setMessage("Informe seu CNPJ e sua senha!",".container-error");
            return false;
        }

        var funcSucess = function(data){            
            if (data.status == 401) {               
                setMessage("Senha ou CNPJ incorreto!",".container-error");              
            }else{
                setMessage("Sucesso! Vamos te redirecionar",".container-error",5000,"bg-success");         
                setTimeout(function(){
                    window.location.href = "/painel_cliente.html";
                },1000)         
            }                  
        }
        var funcError = function(err){
            if (err.status == 401) {
                setMessage("Senha ou CNPJ incorreto!",".container-error");              
            }         
        }

        post_api("login",{"senha":senha,"login":cnpj},funcSucess,funcError)
    });

});