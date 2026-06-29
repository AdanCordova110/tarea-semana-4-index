const formulario = document.getElementById("miFormulario");

const lista = document.getElementById("listaRegistros");

const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;

    if(nombre=="" || descripcion=="" || categoria==""){

        alert("Todos los campos son obligatorios");

        return;

    }

    contador++;

    total.textContent = contador;

    const columna = document.createElement("div");

    columna.className = "col-md-4 mt-3";

    const tarjeta = document.createElement("div");

    tarjeta.className = "card p-3 shadow";

    tarjeta.innerHTML = `
        <h4>${nombre}</h4>
        <p>${descripcion}</p>
        <p><strong>Categoría:</strong> ${categoria}</p>
    `;

    const boton = document.createElement("button");

    boton.textContent = "Eliminar";

    boton.className = "btn btn-danger";

    boton.addEventListener("click", function(){

        columna.remove();

        contador--;

        total.textContent = contador;

    });

    tarjeta.appendChild(boton);

    columna.appendChild(tarjeta);

    lista.appendChild(columna);

    formulario.reset();

});