

$(function(){
   $( ".column" ).sortable({
      connectWith: ".column",
      handle: ".tarjeta-header",
      cancel: ".tarjeta-toggle",
      start: function (event, ui) {
        $(".glyphicon-move", $(ui.item)).toggleClass('hide');
      },
      stop: function (event, ui) {
        $(".glyphicon-move", $(ui.item)).toggleClass('hide');
        var column = $(ui.item).closest(".column").data()["id"];
        var tarjeta = $(ui.item).data()["id"];
        $.get('/tarjeta/' + tarjeta + '/mover/' + column, function() {
            console.log("Movido");
        });
      }
    });
   $( ".ver-tarjeta" ).click(function(e){
        e.preventDefault();
        var id = $(e.currentTarget).data()["id"];
        var title = $(e.currentTarget).data()["title"];
        $('#tarjeta-modal .modal-title').html('<h4 class="modal-title">'+title+'</h4>')
        $('#tarjeta-modal .modal-body').load('/tarjeta/' + id + '/modal/', function(){
            $('#tarjeta-modal').modal();
        });
   });
});

// Capturando el contenedor
var contenedor = document.querySelector('.row.mt-10');

// Capturando todos los elementos con la clase "contColor" dentro del contenedor
var elementosContColor = contenedor.querySelectorAll('.contColor');

// Iterando sobre los elementos y capturando los valores de los atributos data-id
elementosContColor.forEach(function(elemento) {
    var id = elemento.getAttribute('data-id');
   
    if (id == 16) {
        elemento.style.backgroundColor ="#70728F";
    }

    if (id == 17) {
        elemento.style.backgroundColor ="#e44057";
    }

    if (id == 18) {
        elemento.style.backgroundColor ="#e47c40";
    }
    if (id == 19) {
        elemento.style.backgroundColor ="#a8e440";
    }
});

