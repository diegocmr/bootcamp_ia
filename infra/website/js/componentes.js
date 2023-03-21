
function post_api(func, data = null, funcSucess, funcError = false) {

    $.ajax({

        url: 'http://127.0.0.1:8080/' + func,
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data, textStatus, xhr) {
            funcSucess(data);
        },

        error: function (error, textStatus, xhr) {
            if (funcError) {
                funcError(error);
            }
        }
    });

}

clear_message = false;
function setMessage(msg, obj, seconds = 10000, type = "bg-danger", text_color = "text-white") {

    $(obj).show("slow");
    $(obj).children(".message-error").html(msg);
    $(obj).children(".message-error").attr('class', `message-error p-1 text-center text-white ${type} ${text_color}`);

    clearTimeout(clear_message)
    clear_message = setTimeout(function () {
        $(obj).hide("slow");
    }, seconds);
}

function defaultError(err) {

    if (err.status == 401) {
        window.location.href = "/";
    }

}

function includeHTML(js = false) {
    var z, i, elmnt, file, xhttp;
    /* Loop through a collection of all HTML elements: */
    z = document.getElementsByTagName("*");
    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        /*search for elements with a certain atrribute:*/
        file = elmnt.getAttribute("include-html");
        js = elmnt.getAttribute("include-js");
        if (file) {
            /* Make an HTTP request using the attribute value as the file name: */
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        if (js) {
                            $.getScript(js, function () { });
                        }
                        elmnt.innerHTML = this.responseText;
                    }
                    if (this.status == 404) { elmnt.innerHTML = "Page not found."; }
                    /* Remove the attribute, and call this function once more: */
                    elmnt.removeAttribute("include-html");
                    includeHTML();

                }
            }
            xhttp.open("GET", file, true);
            xhttp.send();
            /* Exit the function: */
            return;
        }
    }
}

function open_page() {
    if(window.location.hash == ''|| window.location.hash == null){
        page = "#dashboard";
    }else{
        page = window.location.hash
    }

    $(".page_container").hide();
    $(page).show();
}
function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [day, month, year ].join('/');
}