$(document).ready(function(){
    if(document.domain == "localhost"){
        window.location.href = "http://127.0.0.1:8081/painel_cliente.html";
    }
    includeHTML()
    var funcSucess = function(data){
        console.log(data)
        var cliente = data.cliente;
        $(".client_name").html(cliente.nomeFantasia);
    }
    var funcError = function(err){
        defaultError (err)
    }

    post_api("resumo_cliente",{},funcSucess,funcError)

    $(".nav_list a").click(function(){
        setTimeout(function(){
            open_page();
        },100)        
    })

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
    linkColor.forEach(l=> l.classList.remove('activeMenu'))
    this.classList.add('activeMenu')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))
    
     // Your code to run since DOM is loaded and ready
});