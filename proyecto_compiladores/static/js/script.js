const boton = document.getElementById('btnEnviar');

boton.addEventListener('click', async function() {
    const textoEntrada = document.getElementById('textoEntrada').value;
    const url = '/analizar'; 

    let init = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ source_code: textoEntrada })
    };

    let response = await fetch(url, init);
    let data = await response.json();
    if(response.ok) {
        showResultsOnTable(data.tokens);
    } else {
        if(data.partial_tokens) {
            showResultsOnTable(data.partial_tokens);
        }
        appendErrorToTable(data.error);
    }  
  });

  function showResultsOnTable(tokens) {
    const tablaResultados = document.getElementById('tablaResultados').getElementsByTagName('tbody')[0];
    tablaResultados.innerHTML = '';
    tokens.forEach(token => {
        const fila = tablaResultados.insertRow();
        fila.insertCell(0).innerText = token.value;
        fila.insertCell(1).innerText = token.type;
        fila.insertCell(2).innerText = token.line;
        fila.insertCell(3).innerText = token.column;
    });
}

    function appendErrorToTable(errorMessage) {
        const tablaResultados = document.getElementById('tablaResultados').getElementsByTagName('tbody')[0];
        const fila = tablaResultados.insertRow();
        const cell = fila.insertCell(0);
        cell.colSpan = 4; 
        cell.innerText = `Error: ${errorMessage}`;
        cell.style.color = 'red'; 
    }