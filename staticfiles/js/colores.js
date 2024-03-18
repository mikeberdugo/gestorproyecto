$(document).ready(function() {
    // Espera a que el documento HTML se cargue completamente antes de ejecutar la función

    var table = $("#tabla_riesgos").DataTable({
      // Inicializa la tabla con el ID "matriz" como un objeto DataTable
      searching: true, // Habilita la funcionalidad de búsqueda en la tabla
      language: {
        url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
      },
      // Establece el idioma español para la tabla
      autoWidth: true, // Ajusta automáticamente el ancho de las columnas
      processing: true, // Muestra un mensaje de procesamiento mientras se carga la tabla
      info: false, // Oculta la información de la tabla (por ejemplo, "Mostrando 1 a 10 de 57 registros")
      lengthChange: false, // Oculta el selector de cantidad de registros por página
      scrollX: false, // Deshabilita el desplazamiento horizontal de la tabla
      columnDefs: [
        { targets: [1, 2, 3, 4,5], className: 'dt-body-center' }
      ]
    });

    table.rows().every(function() {
      // Itera sobre cada fila de la tabla

      var data = this.data();
      // Obtiene los datos de la fila actual

      var probabilidad = parseFloat(data[1]);
      // Convierte a número flotante el valor de la segunda columna (Probabilidad)

      var gravedadImpacto = parseFloat(data[2]);
      // Convierte a número flotante el valor de la tercera columna (Gravedad Impacto)

      var valorRiesgo = probabilidad * gravedadImpacto;
      // Calcula el valor de riesgo multiplicando Probabilidad y Gravedad Impacto


      var color = '';
      // Inicializa variables para almacenar el nivel de riesgo y el color correspondiente

      if (valorRiesgo >= 1 && valorRiesgo <= 2) {
        color = 'azul';
      } else if (valorRiesgo >= 3 && valorRiesgo <= 8) {
        color = 'amarillo';
      } else if (valorRiesgo >= 9 && valorRiesgo <= 14) {
        color = 'naranja';
      } else if (valorRiesgo >= 15 && valorRiesgo <= 25) {
        color = 'rojo';
      }
      // Determina el color correspondiente al valor de riesgo calculado

      data[4] = valorRiesgo;
      // Actualiza el valor de la cuarta columna (Valor riesgo) con el valor calculado

      $('td:eq(5)', this.node()).html('<span class="colorestado ' + color + '"></span>');
      // Crea un elemento <span> con la clase "colorestado" y la clase correspondiente al color
      // y lo inserta en la quinta columna (Nivel de riesgo) de la fila actual
    });
  });

