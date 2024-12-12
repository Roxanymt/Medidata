function printPage() {
    window.print();
}


function ContactarAdmin(){
    Swal.fire({
        title: "No tienes permiso para esta opción",
        text: "Debe contactar a un administrador",
        icon: "question",
    });
}


function mostrarTexto() {
    console.log("funciona");
    const select = document.getElementById('exampleFormControlSelect1');
    const textoDescriptivo = document.getElementById('texto-descriptivo');
  
    // Obtener el valor seleccionado
    const opcion = select.value;
  
    // Actualizar el texto basado en la selección
    switch (opcion) {
      case "1":
        textoDescriptivo.textContent = "Criticidad Alta: Problemas críticos que afectan el funcionamiento del sistema y deben solucionarse dentro de las próximas 6 horas.";
        break;
      case "2":
        textoDescriptivo.textContent = "Criticidad Media: Problemas moderados que impactan parcialmente el sistema y se pueden resolver dentro de las próximas 12 horas.";
        break;
      case "3":
        textoDescriptivo.textContent = "Criticidfad Baja: Problemas menores que no afectan significativamente el uso del sistema y se pueden atender dentro de las próximas 24 horas";
        break;
      case "4":
        textoDescriptivo.textContent = "Comparta ideas o recomendaciones para mejorar el sistema y su experiencia como usuario";
        break;
      case "5":
        textoDescriptivo.textContent = "Envíe sus comentarios positivos o reconocimiento por aspectos del sistema que le han gustado";
        break;
      default:
        textoDescriptivo.textContent = "Selecciona una opción para más información.";
        break;
    }
  }