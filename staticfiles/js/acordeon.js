// Obtener todos los elementos del acordeón
var accordionItems = document.querySelectorAll('.accordion-item');

// Agregar un controlador de eventos clic a cada botón del acordeón
accordionItems.forEach(function(item) {
  var button = item.querySelector('.accordion-header');
  var content = item.querySelector('.accordion-content');

  button.addEventListener('click', function() {
    // Alternar la clase 'active' en el elemento del acordeón
    item.classList.toggle('active');

    // Alternar la visibilidad del contenido del acordeón
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
});
