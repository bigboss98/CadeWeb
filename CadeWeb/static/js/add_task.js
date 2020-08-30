$(document).ready(function(){
    //ADD NEW DOCUMENT
    $("#add_document").on("click", function(e){
        e.preventDefault();
        var doc = document.querySelectorAll('.document');
        var $newDocument = '<div class = "document" id = "document-' + (doc.length + 1) + '"> <label for="id_form-' + (doc.length + 1) + '">Document' + (doc.length + 1) + ':</label>' + 
                             '<input type="file" name="form-' + (doc.length + 1) + '-document" id="id_form-' + (doc.length + 1) + '-document"></div>';
        $(".document:last").append($newDocument);
        
    });

    // REMOVE NEW DOCUMENT
    $("#remove_document").on("click", function(e){
        e.preventDefault();
        var documents = document.querySelectorAll('.document');
        if(documents.length > 2){
            $('.document:last').remove();
        }
    });

    // TRAIN NEW TASK
    $('#train').validate({
        submitHandler: function(form){
            form.submit();
        },
        rules: {
            files: {
                required: true,
            }
    
        }
    });
});
