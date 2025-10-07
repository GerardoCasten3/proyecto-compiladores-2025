const boton = document.getElementById('btnEnviar');

boton.addEventListener('click', function() {
    const textoEntrada = document.getElementById('textoEntrada').value;
    const url = '/analizar'; 

    fetch(url, {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ source_code: textoEntrada })
    }).then(response => response.json())
      .then(data => {
          const tablaResultados = document.getElementById('tablaResultados').getElementsByTagName('tbody')[0];
          tablaResultados.innerHTML = ''; // Limpiar la tabla antes de llenarla con nuevos datos
          data.tokens.forEach(token => {
              const fila = tablaResultados.insertRow();
              fila.insertCell(0).innerText = token.value;
              fila.insertCell(1).innerText = token.type;
              fila.insertCell(2).innerText = token.line;
              fila.insertCell(3).innerText = token.column;
          });
      })
      .catch(error => {
          console.error('Error:', error);
      });   
  });