function post_api(func,data = null,funcSucess,funcError = false){

    $.ajax({  
      
        url: 'http://127.0.0.1:8080/'+func,    
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data,textStatus, xhr) {
            funcSucess(data);
            console.log(x);
        },
      
        error: function (error,textStatus, xhr) {
            if(funcError){
                funcError(error);
            }            
        }
    });

}

clear_message = false;
function setMessage (msg, obj, seconds = 10000, type = "bg-danger",text_color = "text-white") {

    $(obj).show("slow");
    $(obj).children(".message-error").html(msg);
    $(obj).children(".message-error").attr('class',`message-error p-1 text-center text-white ${type} ${text_color}`);
   
    clearTimeout(clear_message)
    clear_message = setTimeout(function (){
        $(obj).hide("slow");
    },seconds);
}