const formulario = document.getElementById("miFormulario");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");

let contador = 0;

// Validar nombre
function validarNombre(){

    if(nombre.value.trim().length >= 3){

        nombre.classList.add("is-valid");
        nombre.classList.remove("is-invalid");
        return true;

    }else{

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");
        return false;

    }

}

// Validar descripción
function validarDescripcion(){

    if(descripcion.value.trim().length >= 10){

        descripcion.classList.add("is-valid");
        descripcion.classList.remove("is-invalid");
        return true;

    }else{

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");
        return false;

    }

}

// Validar categoría
function validarCategoria(){

    if(categoria.value!=""){

        categoria.classList.add("is-valid");
        categoria.classList.remove("is-invalid");
        return true;

    }else{

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");
        return false;

    }

}

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

formulario.addEventListener("submit",function(e){

    e.preventDefault();

    const ok1 = validarNombre();
    const ok2 = validarDescripcion();
    const ok3 = validarCategoria();

    if(!(ok1 && ok2 && ok3)){

        mensaje.innerHTML=`
        <div class="alert alert-danger">
        Corrija los campos antes de continuar.
        </div>
        `;

        return;
    }

    contador++;

    total.textContent=contador;

    const columna=document.createElement("div");

    columna.className="col-md-4 mt-3";

    const card=document.createElement("div");

    card.className="card shadow p-3";

    card.innerHTML=`
    <h4>${nombre.value}</h4>
    <p>${descripcion.value}</p>
    <p><strong>Categoría:</strong> ${categoria.value}</p>
    `;

    const boton=document.createElement("button");

    boton.textContent="Eliminar";

    boton.className="btn btn-danger";

    boton.addEventListener("click",function(){

        columna.remove();

        contador--;

        total.textContent=contador;

    });

    card.appendChild(boton);

    columna.appendChild(card);

    lista.appendChild(columna);

    mensaje.innerHTML=`
    <div class="alert alert-success">
    Registro agregado correctamente.
    </div>
    `;

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});