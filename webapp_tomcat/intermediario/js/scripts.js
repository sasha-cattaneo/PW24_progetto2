function submitForm(){
	var link = "./checkConnessioneDB/";

    disableFormElements("#DBconnect");

    var parametri = $("#DBconnect").serializeArray();

    // var t = "";
    // $(parametri).each(function(i, field){
    //     t += field.value;
    //     t += "; ";
    // })
    // console.log("["+t+"]");
    // console.log(parametri);

    if(parametri.length != 6){
        alert("Sono necessari tutti i campi!");
        enableFormElements("#DBconnect"); 
        return;
    }


    $.ajax({
            type: "post",
            url: link,
            async: false,
			data: $.param(parametri),
            success: function (msg) {
                // console.log("SUCCESS");
                alert("Accesso eseguito\nE' possibile importare il DB")
                enableImporta();
            },
            error: function(jqXHR, textStatus, errorThrown) { 
            	alert("Impossibile collegarsi a postgreSQL con i dati inseriti\nControllare che i dati siano corretti")
            }
 	});
    
    return;
}

function enableImporta(){
    $("input[type='submit']").removeAttr("disabled");
}

function disableFormElements(idForm){
    $(idForm).find("input").each(
        function(){
            if($(this).val() ==  "")
                $(this).attr("disabled", "disabled");
        });
}

function enableFormElements(idForm){
    $(idForm).find("input").each(
        function(){
            $(this).removeAttr("disabled");
        });
}

function checkAllCheckbox(this_checkbox, idForm){
    var checkboxAll = this_checkbox;
    var check = checkboxAll.checked;
    $(idForm).find("input[type='checkbox']").not(checkboxAll).each(
        function(){
            $(this).prop('checked', check);
        }
    );
}
