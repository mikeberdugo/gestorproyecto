

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
const contenedor = document.querySelector('.row.mt-10');

// Mapeando los valores de id con sus respectivos colores
const colores = {
  16: "#70728F",
  17: "#e44057",
  18: "#e47c40",
  19: "#a8e440"
};

// Capturando todos los elementos con la clase "contColor" dentro del contenedor
const elementosContColor = contenedor.querySelectorAll('.contColor');

// Iterando sobre los elementos y asignando el color correspondiente
elementosContColor.forEach(elemento => {
  const id = elemento.getAttribute('data-id');
  if (colores[id]) {
    elemento.style.backgroundColor = colores[id];
  }
});
