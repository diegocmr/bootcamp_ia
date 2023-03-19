$(document).ready(function(){

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

document.addEventListener("DOMContentLoaded", function(event) {
   
    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)
    
    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
    toggle.addEventListener('click', ()=>{
    // show navbar
    nav.classList.toggle('show')
    // change icon
    toggle.classList.toggle('bx-x')
    // add padding to body
    bodypd.classList.toggle('body-pd')
    // add padding to header
    headerpd.classList.toggle('body-pd')
    })
    }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header')
    
    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')
    
    function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))
    
     // Your code to run since DOM is loaded and ready
});