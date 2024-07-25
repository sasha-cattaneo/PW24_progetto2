function submitForm(){
    // Inizializzo la variabile link all'URI per la funzione per il controllo della connesione al DB postgreSQL 
	var link = "./checkConnessioneDB/";
    // Disabilito gli input non vuoti nel form "DBconnect"
    disableFormElements("#DBconnect");
    // Salvo tutti gli input abilitati nel form "DBconnect"
    // Cioè i dati per collegarmi al DB postgreSQL
    var parametri = $("#DBconnect").serializeArray();

    // Controllo che tutti gli input siano stati riempiti
    if(parametri.length != 6){
        alert("Sono necessari tutti i campi!");
        enableFormElements("#DBconnect"); 
        return;
    }

    // Chiamata ajax a "link", cioè alla funzione per il controllo della connesione
    // passando i parametri per la connessione
    $.ajax({
            type: "post",
            url: link,
            async: false,
			data: $.param(parametri),
            // Se la connesione ha successo avviso l'utente e abilito l'importo delle tabelle
            success: function (msg) {
                // console.log("SUCCESS");
                alert("Accesso eseguito\nE' possibile importare il DB")
                enableImporta();
            },
            // Se la connessione fallisce avviso l'utente
            error: function(jqXHR, textStatus, errorThrown) { 
            	alert("Impossibile collegarsi a postgreSQL con i dati inseriti\nControllare che i dati siano corretti")
            }
 	});
    
    return;
}
// Abilita ogni submit, cioè abilita l'importo delle tabelle
function enableImporta(){
    $("input[type='submit']").removeAttr("disabled");
}
// Disabilita ogni input in "idForm" con valore ""
function disableFormElements(idForm){
    $(idForm).find("input").each(
        function(){
            if($(this).val() ==  "")
                $(this).attr("disabled", "disabled");
        });
}
// Abilita ogni input in "idForm"
function enableFormElements(idForm){
    $(idForm).find("input").each(
        function(){
            $(this).removeAttr("disabled");
        });
}
// Seleziona/Deseleziona ogni checkbox in "idForm"
function checkAllCheckbox(this_checkbox, idForm){
    var checkboxAll = this_checkbox;
    var check = checkboxAll.checked;
    $(idForm).find("input[type='checkbox']").not(checkboxAll).each(
        function(){
            $(this).prop('checked', check);
        }
    );
}
