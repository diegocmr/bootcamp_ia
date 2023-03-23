$(document).ready(function(){
    if(document.domain == "localhost"){
        window.location.href = "http://127.0.0.1:8081/login.html";
    }
    $(".botao_login").click(function(){
        var cnpj = $("#campo_cnpj").val();
        var senha = $("#campo_senha").val();

        if(cnpj.length < 2 || senha.length < 2){
            setMessage("Informe seu CNPJ e sua senha!",".container-error");
            return false;
        }

        var funcSucess = function(data){            
           
            setMessage("Sucesso! Vamos te redirecionar",".container-error",5000,"bg-success");         
            setTimeout(function(){
                window.location.href = "/painel_cliente.html";
            },1000)         
                            
        }
        var funcError = function(err){
            if (err.status == 401) {
                setMessage("Senha ou CNPJ incorreto!",".container-error");              
            }         
        }

        post_api("login",{"senha":senha,"login":cnpj},funcSucess,funcError)
    });

    $(".botao_cadastro").click(function(){

        var cnpj = $("#cnpj").val();
        var razaoSocial = $("#razaoSocial").val();
        var nomeFantasia = $("#nomeFantasia").val();
        var capitalSocial = tratarFloat($("#capitalSocial").val());
        var totalAtivo = tratarFloat($("#totalAtivo").val());
        var totalPatrimonioLiquido = tratarFloat($("#totalPatrimonioLiquido").val());
        var fataturamentoBruto = tratarFloat($("#fataturamentoBruto").val());
        var senha = $("#senha").val();
        var senha_repetir = $("#senha_repetir").val();
        var empresa_MeEppMei = +$("#empresa_MeEppMei").is(":checked");
        var registerCheck = + $("#registerCheck").is(":checked");
      
        
        if(verificarNull(cnpj)){
            setMessage('Preencha o campo "CNPJ"',".container-error");
            return false;
        }

        if(verificarNull(razaoSocial)){
            setMessage('Preencha o campo "Razão Social"',".container-error");
            return false;
        }

        if(verificarNull(nomeFantasia)){
            setMessage('Preencha o campo "Nome Fantasia"',".container-error");
            return false;
        }

        if(verificarNull(capitalSocial)){
            setMessage('Preencha o campo "Capital Social"',".container-error");
            return false;
        }

        if(verificarNull(totalAtivo)){
            setMessage('Preencha o campo "Total Ativo"',".container-error");
            return false;
        }
        
        if(verificarNull(totalPatrimonioLiquido)){
            setMessage('Preencha o campo "Total Patrimonio Liquido"',".container-error");
            return false;
        }

        if(verificarNull(fataturamentoBruto)){
            setMessage('Preencha o campo "Faturamento Bruto"',".container-error");
            return false;
        }

        if(senha != senha_repetir){
            setMessage("Você não repetiu a senha corretamente",".container-error");
            return false;
        }

        if(verificarNull(senha)){
            setMessage('Preencha o campo "Senha"',".container-error");
            return false;
        }
        
        if(verificarNull(registerCheck)){
            setMessage('Você deve concordar com os termos',".container-error");
            return false;
        }
        
        var data_cadastro = {
            cnpj,
            razaoSocial,
            nomeFantasia,
            capitalSocial,
            totalAtivo,
            totalPatrimonioLiquido,
            fataturamentoBruto,
            senha,
            empresa_MeEppMei,
        }

        var funcSucess = function(data){            
           
            setMessage("Cadastrado com sucesso! Vamos te redirecionar",".container-error",5000,"bg-success");         
            setTimeout(function(){
                window.location.href = "/painel_cliente.html";
            },1000)         
                            
        }

        var funcError = function(err){
           
            setMessage("Ocorreu um erro, tente novamente mais tarde",".container-error");              
                 
        }

        post_api("cadastro_cliente",data_cadastro,funcSucess,funcError)


    });



});