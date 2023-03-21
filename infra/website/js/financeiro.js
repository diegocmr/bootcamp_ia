$(document).ready(function(){
    
    $('#emprestimos').DataTable({
        language: PTBR,
        ajax: {
            url: 'http://127.0.0.1:8080/emprestimos',
            type: 'POST',
            xhrFields: {
                withCredentials: true
            }
        },       
        columns: [
            { title: 'Status',data: 'status' },
            { title: 'Valor Solicitado',data: 'valorSolicitado' },
            { title: 'Valor Aprovado',data: 'valorAprovado' },
            { type: "date-eu" ,title: 'Data', render:function(data, type, row){
                return formatDate((data) ? format_datedata:row["dataAprovadoNivelAnalista"])               
            }}
        ],
        order:[[3, 'desc']]
           
    });

});
