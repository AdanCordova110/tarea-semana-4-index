const formulario = document.getElementById("miFormulario");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");

let contador = 0;
let registros = [];

const contenido = document.getElementById("contenidoDinamico");
const estado = document.getElementById("estadoRegistros");

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

function mostrarRegistros(){

    contenido.innerHTML = "";

    if(registros.length === 0){

        estado.textContent = "No existen registros todavía.";

        return;

    }

    estado.textContent = "";

    registros.forEach((registro, indice)=>{

        const columna = document.createElement("div");

        columna.className = "col-md-4 mt-3";

        columna.innerHTML = `
        <div class="card shadow p-3">

            <h4>${registro.nombre}</h4>

            <p>${registro.descripcion}</p>

            <p><strong>Categoría:</strong> ${registro.categoria}</p>

            <button class="btn btn-danger eliminar" data-id="${indice}">
                Eliminar
            </button>

        </div>
        `;

        contenido.appendChild(columna);

    });

    document.querySelectorAll(".eliminar").forEach(boton=>{

        boton.addEventListener("click",function(){

            registros.splice(this.dataset.id,1);

            contador--;

            total.textContent=contador;

            mostrarRegistros();

        });

    });

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

total.textContent = contador;

registros.push({

    nombre: nombre.value,

    descripcion: descripcion.value,

    categoria: categoria.value

});

mostrarRegistros();

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