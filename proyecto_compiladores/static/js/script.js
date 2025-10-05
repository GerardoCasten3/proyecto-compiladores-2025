const boton = document.getElementById('btnEnviar');

boton.addEventListener('click', function() {
    Swal.fire({
    title: "Exito",
    icon: "success",
    text: 'AQUI VA EL MENSAJE DE EXITO',
    draggable: true
    });
  });