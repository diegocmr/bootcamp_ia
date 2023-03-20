$(document).ready(function(){

    $('#emprestimos').DataTable({
        ajax: {
            url: 'http://127.0.0.1:8080/emprestimos',
            type: 'POST',
        },       
        columns: [
            { emprestimo: 'status' },
            { emprestimo: 'valorSolicitado' },
            { emprestimo: 'valorAprovado' }
        ]
           
    });

});
