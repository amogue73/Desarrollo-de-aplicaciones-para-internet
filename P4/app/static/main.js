const recetas = []              // declaraciones   
let html_str  = ''              // de variables
let i         = 0               //

cargarRecetas()
borrarTodo()

function cargarRecetas() {
while (recetas.length > 0) {
    recetas.pop();
}
html_str = ''
i = 0
// fetch devuelve una promise
fetch('/api/recipes')           // GET por defecto,
.then(res => res.json())        // respuesta en json, otra promise
.then(filas => {                // arrow function
    filas.forEach(fila => {     // bucle ES6, arrow function
        i++
        recetas.push(fila)      // se guardan para después sacar cada una             
        // ES6 templates
        html_str += `<tr>
                       <td>${i}</td>
                       <td>
                          <button onclick="detalle('${i-1}')" 
                                type="button" class="btn boton-nombre btn-outline btn-sm">
                          ${fila.name}
                       </button>
                </td>
                <td>
                <button type="button" onclick="crearModalEditReceta(${i-1})" class="btn btn-warning btn-sm">Editar</button>
                <button type="button" onclick="crearModalBorrarReceta(${i-1})" class="btn btn-danger btn-sm">Borrar</button>
                </td>
                </tr>`         // ES6 templates
    });
    document.getElementById('tbody').innerHTML=html_str  // se pone el html en su sitio
    ponerTamanoLetra()
    ponerModo()


})
}


function detalle(i) {  // saca un modal con la información de cada coctel
  // saca un modal con receta[i]
  let html_str = ''
  html_str +=
  `<div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
          <h1 class="modal-title fs-5">${recetas[i].name}</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <strong>Ingredientes</strong><br /><br />`
        recetas[i].ingredients.forEach(ingredient => {
          html_str += `<p>- ${ingredient.name}</p>`
        });

  html_str += `<br /><strong>Instrucciones</strong><br /><br />`
      recetas[i].instructions.forEach(instruccion => {
        html_str += `<p>${instruccion}</p>`
      })
      
  html_str +=
     ` </div>
    </div>
  </div>`
  document.getElementById('detailModal').innerHTML=html_str

  $(document).ready(function(){
    $("#detailModal").modal('show');
});

}

//Estas variables contienen la información de la receta que se va a añadir
nombreReceta = '' //nombre de la receta
preparacionReceta = [] //array con los pasos de la receta
nombreIngrediente = [] //array con los nombres de los ingredientes
cantidadIngrediente = [] //array con las cantidades de los ingredientes
unidadesIngrediente = [] //array con las unidades de cada cantidad de los ingredientes

//Estas variables contienen la información del nuevo ingrediente que se está añadiendo
nombreIngredienteNuevo = ''
cantidadIngredienteNuevo = ''
unidadesIngredienteNuevo = ''


/**
 * Se prepara un Json con el que se realiza una petición POST para insertar una
 * nueva receta, a partir de los datos proporcionados por el usuario.
 */

function nuevaReceta() {
actualizarReceta()

if (nombreReceta == '' || preparacionReceta.length == 0 || nombreIngrediente.length == 0){

  if (nombreReceta == '' || preparacionReceta.length == 0){
    document.getElementById('errorModalBody').innerHTML = "No se ha insertado la receta. Los campos son obligatorios"
  }

  else if (nombreIngrediente.length == 0){
    document.getElementById('errorModalBody').innerHTML = "No se ha insertado la receta. No se han proporcionado ingredientes" 

  }
  document.getElementById('errorModalBoton').innerHTML = '<button type="button" class="btn btn-primary" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#addRecipeModal">Aceptar</button>'

  $(document).ready(function(){
    $("#errorModal").modal('show');
  });

  borrarDatosReceta()

}
else{

  data = 
  '{"name":"' + nombreReceta + '","instructions":['
    for(let i = 0; i < preparacionReceta.length; i++){
      data = data + '"' + preparacionReceta[i] + '",'
    }
    data = data.slice(0,-1)
    data = data + '],"ingredients":['
    for(let i = 0; i < nombreIngrediente.length; i++){
      data = data + '{"name":' + '"' + nombreIngrediente[i] + '",' +
      '"quantity":{"quantity":' + '"' + cantidadIngrediente[i] + '",' +
      '"unit":' + '"' + unidadesIngrediente[i] + '"}},'
    }
    data = data.slice(0,-1)
    data = data + '],"slug":' + '"'
    slug = nombreReceta.toLowerCase()
    slugSplit = slug.split('\ ')
    for(let i = 0; i < slugSplit.length; i++){
      data = data + slugSplit[i] + '-'
    }
    data = data.slice(0,-1)
    data = data + '"}'


  fetch('/api/recipes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      if(data.hasOwnProperty('error')){
        document.getElementById('errorModalBody').innerHTML = "No se ha insertado la receta. " + data.error
        document.getElementById('errorModalBoton').innerHTML = '<button type="button" class="btn btn-primary" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#addRecipeModal">Aceptar</button>'
        borrarDatosReceta()
        $(document).ready(function(){
          $("#errorModal").modal('show');
        });
      }
      else{
        cargarRecetas()
        borrarTodo()
      }
    })
    .catch((error) => {
      console.error('Error:', error);

    });
  }

}

/**
 * función para preparar el modal con el que se edita una receta
 * 
 */

function crearModalEditReceta(i) {

  html_str = `<button onclick="editReceta(${i})" type="button" class="btn btn-primary" data-bs-dismiss="modal">Confirmar</button>`
  document.getElementById('botonEditReceta').innerHTML=html_str
  document.getElementById('tituloEditRecipeModal').innerHTML='editar: ' + recetas[i].name

  document.getElementById('ingredientesEdit').innerHTML = `<strong>Instrucciones</strong>`

  instrucciones = recetas[i].instructions
  for(let j = 0; j < instrucciones.length; j++){
    str = `<p>${instrucciones[j]}</p>`
    document.getElementById('ingredientesEdit').innerHTML += str

  }


  $(document).ready(function(){
    $("#editRecipeModal").modal('show');
  });
}

/**
 * Se crea un Json para hacer una petición PUT con la que editar una
 * receta, según los datos proporcionados por el usuario 
 *
 */

function editReceta(i) {
  actualizarEditReceta()
  if (nombreReceta != '' || preparacionReceta.length > 0){
    data = '{'
      if (nombreReceta != ''){
        data = data + '"name":"' + nombreReceta + '",' 
      }
      if (preparacionReceta.length > 0){
        data = data + '"instructions":['
        for(let i = 0; i < preparacionReceta.length; i++){
          data = data + '"' + preparacionReceta[i] + '",'
        }
        data = data.slice(0,-1)
        data = data + '],'
      }
      data = data.slice(0,-1)
      data += '}'

    url_str = '/api/recipes/' + recetas[i]._id
    fetch(url_str, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        if(data.hasOwnProperty('error')){
          document.getElementById('errorModalBody').innerHTML = "No se ha actualizado la receta. " + data.error
          document.getElementById('errorModalBoton').innerHTML = '<button type="button" class="btn btn-primary" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#editRecipeModal">Aceptar</button>'
          borrarDatosReceta()
          $(document).ready(function(){
            $("#errorModal").modal('show');
          });
        }
        else{
          cargarRecetas()
          borrarTodo()
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        borrarTodo()

      });
  }
}

/**
 * Función que crea el modal para confirmar el borrado de una receta
 * 
 */

function crearModalBorrarReceta(i){
  html_str = `<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
  <button onclick="borrarReceta(${i})" type="button" class="btn btn-primary" data-bs-dismiss="modal">Confirmar</button>`
  document.getElementById('botonBorrarReceta').innerHTML=html_str
  document.getElementById('tituloBorrarRecetaModal').innerHTML='borrar: ' + recetas[i].name

    $(document).ready(function(){
      $("#borrarRecetaModal").modal('show');
  });
}

/**
 * Función que hace una petición DELETE para borrar una receta
 * 
 */

function borrarReceta(i) {
  url_str = '/api/recipes/' + recetas[i]._id
  fetch(url_str, {
    method: 'DELETE'

  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      cargarRecetas()
      borrarTodo()
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/**
 * Función que añade los datos de un nuevo ingrediente a los arrays de ingredientes correspondientes
 * 
 */

function nuevoIngrediente() {
  actualizarIngredientes()

  //se comprueba si algún campo está vacío, si es así se muestra un error
  if (nombreIngredienteNuevo == '' || cantidadIngredienteNuevo == '' || unidadesIngredienteNuevo == ''){
    document.getElementById('errorModalBody').innerHTML = "No se ha guardado el ingrediente. Los campos son obligatorios"
    document.getElementById('errorModalBoton').innerHTML = '<button type="button" class="btn btn-primary" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#addIngredientModal">Aceptar</button>'

    $(document).ready(function(){
      $("#errorModal").modal('show');
    });
  }
  else{

    nombreIngrediente.push(nombreIngredienteNuevo)
    cantidadIngrediente.push(cantidadIngredienteNuevo)
    unidadesIngrediente.push(unidadesIngredienteNuevo)

    //se borran los campos en el modal de añadir ingrediente
    borrarTextoIng() 
    //se añade el ingrediente correspondiente al modal de nueva receta a modo de información
    document.getElementById('ingredientes').innerHTML = `<strong>Ingredientes</strong>`

    for(let i = 0; i < nombreIngrediente.length; i++){
      str = `<p> - ${nombreIngrediente[i]}: ${cantidadIngrediente[i]} ${unidadesIngrediente[i]}</p>`
      document.getElementById('ingredientes').innerHTML += str
    }
    $(document).ready(function(){
      $("#addRecipeModal").modal('show');
    });
  }
}

/**
 * función que elimina los caracteres \n, \r y \t de una string
 * y los espacios en blanco anteriores a la izquierda del primer
 * caracter que no pertenezca a estos
 * 
 */
function limpiarStr(str){
  str_limpia = ''
  vacia = true
  for(let i = 0; i < str.length; i++){
    if (str[i] != '\n' && str[i] != '\r' && str[i] != '\t'){
      if (vacia){
        if (str[i] != '\ '){
          vacia = false
          str_limpia += str[i]
        }
      }else{
          str_limpia += str[i]
      }
    }
  }
  return str_limpia
}

/**
 * función que crea el array de pasos de preparación de una receta
 * a partir de un solo string.
 * los pasos se separan por <<.>>
 */
function crearPreparacion(str_prep){
  paso = ''
  for(let i = 0; i < str_prep.length; i++){
    if (str_prep[i] != '\n' && str_prep[i] != '\r' && str_prep[i] != '\t')
      paso += str_prep[i]
    if (str_prep[i] == '.' || i == (str_prep.length-1)){
      if (str_prep[i] == '.')
        paso = paso.slice(0,-1)
      preparacionReceta.push(paso)
      paso = ''
    }
  }

  if (preparacionReceta == "")
    preparacionReceta = []
}


/**
 * función que asigna a las variables nombreReceta y preparacionReceta
 * los valores obtenidos a partir de los datos introducidos en los campos
 * correspondientes cuando se está añadiendo una receta
 */
function actualizarReceta() {
  var fields = $( "textarea" ).serializeArray();

  jQuery.each(fields, function(i, field) {
    if (field.name == "nombreReceta")
      nombreReceta = limpiarStr(field.value)
    else if (field.name == "preparacion"){
      crearPreparacion(field.value)
    }


  })

}

/**
 * función análoga a la anterior pero para editar una receta
 */

function actualizarEditReceta() {
  var fields = $( "textarea" ).serializeArray();

  jQuery.each(fields, function(i, field) {
    if (field.name == "nombreEditReceta")
      nombreReceta = limpiarStr(field.value)
    else if (field.name == "editPreparacion"){
      crearPreparacion(field.value)
    }
  })
}


/**
 * función que actualiza las variables de los datos del ingrediente
 * que se está añadiendo con los valores introducidos por el usuario
 */
function actualizarIngredientes() {
  var fields = $( "textarea" ).serializeArray();

  jQuery.each(fields, function(i, field) {

  if (field.name == "nombreIngrediente")
    nombreIngredienteNuevo = limpiarStr(field.value)
  else if (field.name == "cantidad")
    cantidadIngredienteNuevo = limpiarStr(field.value)
  else if (field.name == "unidades")
    unidadesIngredienteNuevo = limpiarStr(field.value)

  })
}


function borrarDatosReceta(){
  nombreReceta = ''
  preparacionReceta = []
}

function borrarDatos(){
  nombreReceta = ''
  preparacionReceta = []
  nombreIngrediente = []
  cantidadIngrediente = []
  unidadesIngrediente = []
}

/**
 * función que anula las variables correspondientes a los datos
 * de la nueva receta, todos los campos de datos y las lista de los ingredientes 
 * de los modales de nueva receta y de editar receta
 */
function borrarTodo() {
  textos = document.getElementsByClassName("texto")
  for(let i = 0; i < textos.length; i++){
    textos[i].value = ""
  }

  borrarDatos()

  document.getElementById('ingredientes').innerHTML = ''
  document.getElementById('ingredientesEdit').innerHTML = ''

}

/**
 * función que borra los campos del modal de nuevo ingrediente
 */

function borrarTextoIng() {
  textos = document.getElementsByClassName("texto ing")
  for(let i = 0; i < textos.length; i++){
    textos[i].value = ""
  } 
}

/**
 * función que actualiza los elementos de la página web según el tamaño de
 * letra guardado en localStorage
 */

function ponerTamanoLetra(){
  valor = localStorage.getItem('letra')

  let tamLetra = '1em'

  if (valor != null){
    if (valor == 0)
      tamLetra = '0.9em'
    else if(valor == 1)
      tamLetra = '1em'
    else if(valor == 2)
      tamLetra = '1.1em'
  }

  modals = document.getElementsByClassName("modal")
  for(let i = 0; i < modals.length; i++){
    modals[i].style.fontSize=tamLetra
  }

  buttons = document.getElementsByTagName("button")
  for(let i = 0; i < buttons.length; i++){
    buttons[i].style.fontSize=tamLetra
  }

  tables = document.getElementsByTagName("table")
  for(let i = 0; i < tables.length; i++){
    tables[i].style.fontSize=tamLetra
  }
}

/**
 * función que cambia el valor del item letra de localstorage
 * y que actualiza el tamaño de la letra de la página
 */

function cambiarLetra(){

  valor = localStorage.getItem('letra')

  if (valor == null){
    valor = 2
    localStorage.setItem('letra',2)
  }
  else{
    valor = (valor+1)%3
    localStorage.setItem('letra',valor)
  }
  ponerTamanoLetra()
}

/**
 * función que cambia el tema de la página (claro u oscuro)
 * según la preferencia guardada en el item modo de localstorage
 */

function ponerModo(){
  valor = localStorage.getItem('modo')
  let modoColor = 'light'
  botones = document.getElementsByClassName("boton-nombre")


  if (valor != null){
    if (valor == 0){
      modoColor = 'light'
      for(let i = 0; i < botones.length; i++){
        botones[i].setAttribute("class","btn boton-nombre btn-outline btn-sm")
      }
    }
    else if(valor == 1){
      modoColor = 'dark'
      for(let i = 0; i < botones.length; i++){
        botones[i].setAttribute("class","btn boton-nombre btn-outline btn-sm btn-dark")
      }
    }
  }

  document.getElementById("documento").setAttribute("data-bs-theme",modoColor)

}

/**
 * función que cambia el valor del item modo de localstorage y que
 * cambia el tema de la página
 */

function cambiarModo(){

  valor = localStorage.getItem('modo')
  
  if (valor == null){
    valor = 1
    localStorage.setItem('modo',1)
  }
  else{
    valor = (parseInt(valor)+1)%2
    localStorage.setItem('modo',valor)
  }
  ponerModo()
}



