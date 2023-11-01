let pagina = 1;
let pagina_empresa = 1;
let pag_user_empre = 1;
let pagina_rol = 1;
let pagina_empleado = 1;
let pag_empl_empre = 1;
let pagina_nomina = 1;
let pagina_nominass = 1;
let pagina_prestamo = 1;
const registrosPorPagina = 10;
const row_empresa = 10;
const row_rol = 10;
const row_nomina = 10;
const row_prestamo = 10;
const row_user_empre = 10;
const row_empleado = 10;
const row_empl_empre = 10;

// Eventos botones para tabla dinamica usuarios
// --------------------------------------------

function mostrarMasUsuarios() {
    pagina++;
    get_usuarios();
}

function regresarUsuarios() {
    if (pagina > 1) {
        pagina--;
        get_usuarios();
    }
}

// --------------------------------------------------------
// Funcion para obtener la lista de todos los usuarios
// --------------------------------------------------------
function get_usuarios() {
    fetch('/usuarios', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataUsuario(data))
        .catch(error => console.log(error))
}

// --------------------------------------------------------
// Funcion para mostrar datos de usuarios en tabla html
// --------------------------------------------------------
function mostrarDataUsuario(data) {
    //console.log(data)
    data = data.usuarios
    let body = ""
    const inicio = (pagina - 1) * registrosPorPagina;
    const fin = pagina * registrosPorPagina;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            if (data[i].estado === 0) {
                data[i].estado = '<span class="badge badge-success">Activo</span>'
            }
            body += `<tr><td>${data[i].id_usuario}</td><td>${data[i].usuario}</td>
                            <td>${data[i].f_registro}</td><td>${data[i].f_modificacion}</td><td>${data[i].nombre_rol}</td>
                            <td>${data[i].id_empresa}</td><td>${data[i].nombre_empresa}</td><td>${data[i].estado}</td><td>
                            <button onclick="editar_usuario(${data[i].id_usuario}, ${data[i].id_rol})" class="btn btn-warning"><ion-icon name="create-outline"></ion-icon></button>
                            <button onclick="eliminar_usuario(${data[i].id_usuario})" class="btn btn-danger"><ion-icon name="trash-outline"></ion-icon></button>
                            <button onclick="" class="btn btn-primary" </button>ver</td></tr>`
        }
    }
    document.getElementById('data').innerHTML = body;
}

vercadena = document.getElementById('data');

// console.log(vercadena);

// --------------------------------------------------------
// Funcion para mostrar lista de roles
// --------------------------------------------------------
function get_roles_select(tipo_select, defaultRolId = null, dashboard = null) {
    const type = tipo_select
    fetch('/roles', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(type);
            select.innerHTML = ''; // Eliminar el mensaje de "Cargando roles..."
            //console.log(data)
            data = data.roles

            if (dashboard) {
                data.forEach(rol => {
                    const option = document.createElement('option');
                    if (rol.id_rol === 3) {
                        option.value = rol.id_rol;
                        option.textContent = rol.nombre_rol;
                        select.appendChild(option);
                    }
                }
                );
            } else {
                data.forEach(rol => {
                    const option = document.createElement('option');
                    option.value = rol.id_rol; // Asigna el valor que desees
                    option.textContent = rol.nombre_rol; // Asigna el texto que desees
                    // Establece el valor seleccionado si coincide con el valor por defecto proporcionado
                    if (defaultRolId && rol.id_rol === defaultRolId) {
                        option.selected = true;
                    }
                    select.appendChild(option);

                });
            }
        }
        )
        .catch(error => console.log(error))
}
// ---------------------------------
// Generar contraseñas de 10 digitos
// --------------------------------- 
function generarPassword(id_input) {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let contrasena = '';
    const longitud = 10; // Cambia la longitud de la contraseña según tus necesidades

    for (let i = 0; i < longitud; i++) {
        const caracterAleatorio = caracteres.charAt(Math.floor(Math.random() * caracteres.length));
        contrasena += caracterAleatorio;
    }

    const btnPass = document.getElementById(id_input)
    btnPass.value = contrasena;
}


// -------------------------------------------------
// Función para validar usuario que tengo solo texto
// -------------------------------------------------
function validarCadena(cadena) {
    // Expresión regular que verifica si la cadena contiene espacios, números o signos
    const expresionRegular = /[0-9\s!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/;

    if (expresionRegular.test(cadena)) {
        // La cadena contiene espacios, números o signos, no se acepta
        return false;
    } else {
        // La cadena no contiene espacios, números ni signos, se acepta
        return true;
    }
}

// --------------------------------------------------------
// Funcion para agregar usuarios por medio de servicio
// --------------------------------------------------------
function add_usuario() {
    const _usuario = document.getElementById('usuario').value;
    const _password = document.getElementById('password').value;
    const _rol = document.getElementById('selectRoles').value;
    const _empresa = document.getElementById('selectEmpresa').value;

    if (!_usuario || !_password || !_rol) {
        alert("Por favor, complete todos los campos.");
        resetForm('isertar_usuario');
        generarPassword()
        return;
    }

    if (!(_usuario.length >= 3 && _usuario.length <= 20)) {
        alert("Longitud no aceptable, mínimo 3 caracteres y máximo 20 caracteres");
        resetForm('isertar_usuario');
        generarPassword()
        return;
    }

    if (!validarCadena(_usuario)) {
        alert("Usuario invalido, ingresar solo texto.");
        resetForm('isertar_usuario');
        generarPassword()
        return;
    }

    // armar el body 
    const _body = { usuario: _usuario, password: _password, rol: _rol, empresa: _empresa }

    // Header por default
    const _header = { "Content-Type": "application/json" }

    fetch('/insert_usuario', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            if (response.mensaje === 'Usuario agregado exitosamente') {
                location.reload(true);
            }
            //console.log(response);
            resetForm('isertar_usuario'); // id de formulario como parametro
            generarPassword()
        })
        .catch((error) => console.error("Error", error))
}

// --------------------------------------------------------
// Funcion para resetear un formulario especifico
// --------------------------------------------------------
function resetForm(formulario) {
    // Obtén el formulario por su ID o de alguna otra manera
    const form = document.getElementById(formulario);

    // Restablece el formulario
    form.reset();
}


// --------------------------------------------------------
// Funcion para rellenar el formulario de editar usuario
// --------------------------------------------------------
function editar_usuario(id_usuario, id_rol) {
    fetch('/usuarios/' + id_usuario, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            data = data.Usuario;
            document.getElementById("id_usuario").value = data.id_usuario;
            document.getElementById("editUsuario").value = data.usuario;
            document.getElementById("editPassword").value = data.password;

            if (data.identidad === 1) {
                get_roles_select('selectEditRoles', id_rol);
                get_select_empresas('selectEditEmpresa', data.id_empresa, data.identidad);
            } else {
                get_roles_select('selectEditRoles', null, data.identidad);
                get_select_empresas('selectEditEmpresa', data.id_empresa);
            }

            $('#modal_editar').modal('show');
        })
        .catch(error => console.log(error))
}

// --------------------------------------------------------
// Funcion para actualizar un usuario
// --------------------------------------------------------
function actualizar_usuario() {
    const _id = document.getElementById('id_usuario').value;
    const _usuario = document.getElementById('editUsuario').value;
    const _password = document.getElementById('editPassword').value;
    const _rol = document.getElementById('selectEditRoles').value;
    const _empresa = document.getElementById('selectEditEmpresa').value;

    if (!_id || !_usuario || !_password || !_rol || !_empresa) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    // armar el body 
    const _body = { usuario: _usuario, password: _password, rol: _rol, id: _id, empresa: _empresa }
    //console.log(_body)
    // Header por default
    const _header = { "Content-Type": "application/json" }

    fetch('/update_usuario', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            resetForm('actualizar_usuario'); // id de formulario como parametro
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}

// --------------------------------------------------------
// Funcion para eliminar un usuario
// --------------------------------------------------------
function eliminar_usuario(id_usuario) {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
        // Enviar solicitud para eliminar el registro
        fetch('/delete_usuario/' + id_usuario)
            .then(res => res.json())
            .then(response => {
                alert(response.mensaje);
                //console.log(response);
                location.reload(true);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
}


// Eventos botones para tabla dinamica empresa
// --------------------------------------------
function mostrarMasEmpresa() {
    pagina_empresa++;
    get_empresas();
}

function regresarEmpresa() {
    if (pagina_empresa > 1) {
        pagina_empresa--;
        get_empresas();
    }
}


// --------------------------------------------------------
// Funcion Buscar. SEARCH
// --------------------------------------------------------

function Search() {

    const buscador = document.getElementById('searchInput');
    const miTabla = document.getElementById('miTabla');
    const filas = document.getElementsByTagName('tr');

    buscador.addEventListener('input', () => {
        const buscadorText = buscador.value.toLowerCase();

        for (let i = 1; i < filas.length; i++) {
            const fila = filas[i];
            const DatoUsuario = fila.textContent.toLowerCase();

            if (DatoUsuario.includes(buscadorText)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }

        }
    });

}




// --------------------------------------------------------
// Funcion para obtener la lista de todas las empresas
// --------------------------------------------------------
function get_empresas() {
    fetch('/empresas', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataEmpresas(data))
        .catch(error => console.log(error))
}

// --------------------------------------------------------
// Funcion para mostrar datos de empresas en tabla html
// --------------------------------------------------------
function mostrarDataEmpresas(data) {
    //console.log(data)
    data = data.empresas
    let body = ""
    const inicio = (pagina_empresa - 1) * row_empresa;
    const fin = pagina_empresa * row_empresa;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            if (data[i].estado === 0) {
                data[i].estado = '<span class="badge badge-success">Activo</span>'
            }

            body += `<tr><td>${data[i].id_empresa}</td><td>${data[i].nombre_empresa}</td>
                            <td>${data[i].fecha_ingreso}</td><td>${data[i].estado}</td>
                            <td>
                            <button onclick="editar_empresa(${data[i].id_empresa})" class="btn btn-warning"><ion-icon name="create-outline"></ion-icon></button>
                            <button onclick="eliminar_empresa(${data[i].id_empresa})" class="btn btn-danger"><ion-icon name="trash-outline"></ion-icon></button></td></tr>`
        }
    }
    document.getElementById('data_empresa').innerHTML = body;
}

// --------------------------------------------------------
// Funcion para rellenar el formulario de editar empresa
// --------------------------------------------------------
function editar_empresa(id_empresa) {
    fetch('/empresa/' + id_empresa, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            data = data.Empresa;
            //console.log(data)
            document.getElementById("id_empresa").value = data.id_empresa;
            document.getElementById("editEmpresa").value = data.nombre_empresa;
            $('#modal_editar_empresa').modal('show');
        })
        .catch(error => console.log(error))
}

// --------------------------------------------------------
// Funcion para agregar empresa por medio de servicio
// --------------------------------------------------------
function add_empresa() {
    const _empresa = document.getElementById('nombre_empresa').value;


    if (!_empresa) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    if (!(_empresa.length >= 3 && _empresa.length <= 20)) {
        alert("Longitud no aceptable, mínimo 3 caracteres y máximo 20 caracteres");
        resetForm('isertar_empresa');
        return;
    }

    if (!validarCadena(_empresa)) {
        alert("Usuario invalido, ingresar solo texto.");
        resetForm('isertar_empresa');
        return;
    }
    // armar el body 
    const _body = { empresa: _empresa }

    // Header por default
    const _header = { "Content-Type": "application/json" }

    fetch('/insert_empresa', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            if (response.mensaje === 'Empresa agregado exitosamente') {
                location.reload(true);
            }
            resetForm('isertar_empresa'); // id de formulario como parametro

        })
        .catch((error) => console.error("Error", error))
}

// --------------------------------------------------------
// Funcion para mostrar lista de roles
// --------------------------------------------------------
function get_select_empresas(tipo_select, defaultIdEmpresa = null, dashboard = null) {
    const type = tipo_select
    fetch('/empresas', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(type);
            select.innerHTML = ''; // Eliminar el mensaje de "Cargando roles..."
            //console.log(data)
            data = data.empresas

            if (defaultIdEmpresa && dashboard === null) {
                data.forEach(empresa => {
                    const option = document.createElement('option');
                    if (empresa.id_empresa === defaultIdEmpresa) {
                        option.value = empresa.id_empresa;
                        option.textContent = empresa.nombre_empresa;
                        select.appendChild(option);
                    }
                });
            } else {
                data.forEach(empresa => {
                    const option = document.createElement('option');
                    option.value = empresa.id_empresa;
                    option.textContent = empresa.nombre_empresa;

                    // Establece el valor seleccionado si coincide con el valor por defecto proporcionado
                    if (dashboard && empresa.id_empresa === defaultIdEmpresa) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
            }
        })
        .catch(error => console.log(error))
}

function get_select_usuarios(tipo_select, defaultIdUsuario = null, dashboard = null) {
    const type = tipo_select
    fetch('/usuarios_empresas', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            const select = $(`#${type}`);
            

            // Agregar las opciones al select utilizando Select2
            select.select2({
                data: data.usuarios.map(usuario => ({
                    id: usuario.id_usuario,
                    text: usuario.usuario
                })),
                placeholder: 'Selecciona un usuario',
                allowClear: true
            });

            // Establecer el valor seleccionado si se proporciona un valor por defecto
            if (defaultIdUsuario !== null) {
                select.val(defaultIdUsuario).trigger('change');
            }
        })
        .catch(error => console.error('Error al obtener usuarios:', error));
}


// --------------------------------------------------------
// Funcion para actualizar una empresa
// --------------------------------------------------------
function actualizar_empresa() {
    const _id = document.getElementById('id_empresa').value;
    const _empresa = document.getElementById('editEmpresa').value;


    if (!_id || !_empresa) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    // armar el body 
    const _body = { id: _id, empresa: _empresa }
    //console.log(_body)
    // Header por default
    const _header = { "Content-Type": "application/json" }

    fetch('/update_empresa', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            resetForm('actualizar_empresa'); // id de formulario como parametro
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}


// --------------------------------------------------------
// Funcion para eliminar una empresa
// --------------------------------------------------------
function eliminar_empresa(id_empresa) {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
        // Enviar solicitud para eliminar el registro
        fetch('/delete_empresa/' + id_empresa)
            .then(res => res.json())
            .then(response => {
                alert(response.mensaje);
                //console.log(response);
                location.reload(true);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
}


// ################################################################################################
// Eventos botones para tabla dinamica usuarios de empresa
// --------------------------------------------

function mostrarMasUsuariosEmpre() {
    pagina++;
    get_usuarios_Empre();
}

function regresarUsuariosEmpre() {
    if (pagina > 1) {
        pagina--;
        get_usuarios_Empre();
    }
}

// --------------------------------------------------------
// Funcion para obtener la lista de todos los usuarios
// --------------------------------------------------------
function get_usuarios_Empre() {
    fetch('/usuarios_empresas', { method: 'GET' })
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo obtener la respuesta esperada.');
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                mostrarDataUsuario(data);
            } else {
                console.log('Los datos recibidos no son válidos.');
            }
        })
        .catch(error => console.error('Error en la solicitud:', error));
}


//---------------------------------------------------------------**
//---------------------------------------------------------------**
//------------------------MODULO DE ROLES------------------------**
//---------------------------------------------------------------**
//---------------------------------------------------------------**


// Funciones para botones de tabla dinamica de roles
//---------------------------------------------------------------
function mostrarMasRoles() {
    pagina_rol++;
    get_roles();
}

function regresarRoles() {
    if (pagina_rol > 1) {
        pagina_rol--;
        get_roles();
    }
}

// Funcion para obtener la lista de todos los roles
//---------------------------------------------------------------
function get_roles() {
    fetch('/roles', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataRoles(data))
        .catch(error => console.log(error))
}

// Funcion para mostrar los datos de los roles en tabla html
//---------------------------------------------------------------
function mostrarDataRoles(data) {
    //console.log(data)
    data = data.roles
    let body = ""
    const inicio = (pagina_rol - 1) * row_rol;
    const fin = pagina_rol * row_rol;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            if (data[i].estado === 0) {
                data[i].estado = '<span class="badge badge-success">Activo</span>'
            }
            body += `<tr>
                        <td>${data[i].id_rol}</td>
                        <td>${data[i].nombre_rol}</td>
                        <td>${data[i].estado}</td>
                        <td>
                            <button onclick="editar_rol(${data[i].id_rol})" class="btn btn-warning"><ion-icon name="create-outline"></ion-icon></button>
                            <button onclick="eliminar_rol(${data[i].id_rol})" class="btn btn-danger"><ion-icon name="trash-outline"></ion-icon></button>
                        </td>
                    </tr>`
        }
    }
    document.getElementById('data_rol').innerHTML = body;
}

// Funcion para rellenar el formulario de editar rol
//---------------------------------------------------------------
function editar_rol(id_rol) {
    fetch('/rol/' + id_rol, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            data = data.Rol;
            //console.log(data)
            document.getElementById("id_rol").value = data.id_rol;
            document.getElementById("editRol").value = data.nombre_rol;
            $('#modal_editar_rol').modal('show');
        })
        .catch(error => console.log(error))
}

// Funcion para agregar rol
//---------------------------------------------------------------
function add_rol() {
    const _rol = document.getElementById('nombre_rol').value;
    if (!_rol) {
        alert("Por favor, complete todos los campos.");
        return;
    }
    // armar el body 
    const _body = { rol: _rol }
    // Header por default
    const _header = { "Content-Type": "application/json" }
    fetch('/insert_rol', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            resetForm('isertar_rol'); // id de formulario como parametro
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}

// Funcion para actualizar rol
//---------------------------------------------------------------
function actualizar_rol() {
    const _id = document.getElementById('id_rol').value;
    const _rol = document.getElementById('editRol').value;
    if (!_id || !_rol) {
        alert("Por favor, complete todos los campos.");
        return;
    }
    // armar el body 
    const _body = { id: _id, rol: _rol }
    //console.log(_body)
    // Header por default
    const _header = { "Content-Type": "application/json" }
    fetch('/update_rol', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            resetForm('actualizar_rol'); // id de formulario como parametro
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}

//Funcion para eliminar rol
//---------------------------------------------------------------
function eliminar_rol(id_rol) {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
        // Enviar solicitud para eliminar el registro
        fetch('/delete_rol/' + id_rol)
            .then(res => res.json())
            .then(response => {
                alert(response.mensaje);
                //console.log(response);
                location.reload(true);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
}

// --------------------------------------------------------
// Funcion para mostrar empresa que inicia sesion
// --------------------------------------------------------
function get_nombre_empresa(tipo_select) {
    const type = tipo_select
    fetch('/nombre_empresa', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            data = data.empresa
            const select = document.getElementById(type);
            select.innerHTML = '';
            const option = document.createElement('option');
            option.value = data.id_empresa;
            option.textContent = data.nombre_empresa;
            select.appendChild(option);
        })
        .catch(error => console.log(error))
}



//---------------------------------------------------------------**
//---------------------------------------------------------------**
//--------------------MODULO DE DEPARTAMENTOS--------------------**
//---------------------------------------------------------------**
//---------------------------------------------------------------**


// Funciones para botones de tabla dinamica de departamentos
//---------------------------------------------------------------
function siguienteDepartamentos() {
    pagina++;
    get_departamentos();
}

function regresarDepartamentos() {
    if (pagina > 1) {
        pagina--;
        get_departamentos();
    }
}

// Funcion para obtener la lista de todos los departamentos
//---------------------------------------------------------------
function get_departamentos() {
    fetch('/departamentos', { method: 'GET' })
        .then(response => response.json())
        .then(data => siguientedepartamentos(data))
        .catch(error => console.log(error))
}

// Funcion para mostrar los datos de los departamentos en tabla html
//---------------------------------------------------------------
function mostrarDataDepartamentos(data) {
    //console.log(data)
    data = data.departamentos
    let body = ""
    const inicio = (pagina_departamento - 1) * row_departamento;
    const fin = pagina_departamento * row_departamento;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            if (data[i].estado === 0) {
                data[i].estado = '<span class="badge badge-success">Activo</span>'
            }
            body += `<tr>
                        <td>${data[i].id_departamento}</td>
                        <td>${data[i].nombre_departamento}</td>
                        <td>${data[i].estado}</td>
                        <td>
                            <button onclick="editar_departamento(${data[i].id_departamento})" class="btn btn-warning"><ion-icon name="create-outline"></ion-icon></button>
                            <button onclick="eliminar_departamento(${data[i].id_departamento})" class="btn btn-danger"><ion-icon name="trash-outline"></ion-icon></button>
                        </td>
                    </tr>`
        }
    }
    document.getElementById('data_departamento').innerHTML = body;
}

// Funcion para rellenar el formulario de editar departamento
//---------------------------------------------------------------
function editar_departamento(id_departamento) {
    fetch('/departamento/' + id_departamento, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            data = data.Departamento;
            //console.log(data)
            document.getElementById("id_departamento").value = data.id_departamento;
            document.getElementById("editDepartamento").value = data.nombre_departamento;
            $('#modal_editar_departamento').modal('show');
        })
        .catch(error => console.log(error))
}

// Funcion para agregar departamento
//---------------------------------------------------------------
function add_departamento() {
    const _departamento = document.getElementById('departamento').value;
    const _id_usuario = document.getElementById('selectUsuarios').value;

    if (!_usuario || !_password || !_rol) {
        alert("Por favor, complete todos los campos.");
        resetForm('isertar_usuario');
        generarPassword()
        return;
    }

    // armar el body 
    const _body = { departamento: _departamento, password: _password, rol: _rol}

    // Header por default
    const _header = { "Content-Type": "application/json" }

    fetch('/insert_departamento', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            if (response.mensaje === 'Usuario agregado exitosamente') {
                location.reload(true);
            }
            //console.log(response);
            resetForm('isertar_usuario'); // id de formulario como parametro
            generarPassword()
        })
        .catch((error) => console.error("Error", error))
}

// Funcion para actualizar departamento
//---------------------------------------------------------------
function actualizar_departamento() {
    const _id = document.getElementById('id_departamento').value;
    const _departamento = document.getElementById('editDepartamento').value;
    if (!_id || !_departamento) {
        alert("Por favor, complete todos los campos.");
        return;
    }
    // armar el body 
    const _body = { id: _id, departamento: _departamento }
    //console.log(_body)
    // Header por default
    const _header = { "Content-Type": "application/json" }
    fetch('/update_departamento', {
        method: "POST",
        body: JSON.stringify(_body),
        headers: _header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            //console.log(response);
            resetForm('actualizar_departamento'); // id de formulario como parametro
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}

//Funcion para eliminar departamento
//---------------------------------------------------------------
function eliminar_departamento(id_departamento) {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
        // Enviar solicitud para eliminar el registro
        fetch('/delete_departamento/' + id_departamento)
            .then(res => res.json())
            .then(response => {
                alert(response.mensaje);
                //console.log(response);
                location.reload(true);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
}

function mostrarMasEmpleados() {
    pagina_empleado++;
    get_empleados();
}

function regresarEmpleados() {
    if (pagina_empleado > 1) {
        pagina_empleado--;
        get_empleados();
    }
}


// --------------------------------------------------------
// Funcion para obtener la lista de todos los empleados
// --------------------------------------------------------
function get_empleados() {
    fetch('/empleados', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataEmpleado(data))
        .catch(error => console.log(error))
}

// --------------------------------------------------------
// Funcion para mostrar datos de empleados en tabla html
// --------------------------------------------------------
function mostrarDataEmpleado(data) {
    console.log(data)
    data = data.empleados
    let body = ""
    const inicio = (pagina_empleado - 1) * row_empleado;
    const fin = pagina_empleado * row_empleado;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            if (data[i].estado === 0) {
                data[i].estado = '<span class="badge badge-success">Activo</span>'
            }
            body += `<tr><td>${data[i].id_empleado}</td><td>${data[i].nombre}</td><td>${data[i].apellido}</td>
                            <td>${data[i].dpi}</td><td>${data[i].nit}</td>
                            <td>${data[i].telefono}</td><td>${data[i].correo}</td><td>${data[i].estado}</td>
                            <td>${data[i].nombre_empresa}</td><td>${data[i].puesto}</td><td>
                            <button onclick="editar_empleado(${data[i].id_empleado}, ${data[i].id_rol})" class="btn btn-warning"><ion-icon name="create-outline"></ion-icon></button>
                            <button onclick="eliminar_empleado(${data[i].id_empleado})" class="btn btn-danger"><ion-icon name="trash-outline"></ion-icon></button>
                            </td></tr>`
        }
    }
    document.getElementById('data').innerHTML = body;
}

function validarCorreo(correo) {
    let expresionRegular = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return expresionRegular.test(correo);
}

function validarFormulario() {
    const nombres = document.getElementById("nombres").value;
    const apellidos = document.getElementById("apellidos").value;
    const dpi = document.getElementById("dpi").value;
    const nit = document.getElementById("nit").value;
    const direccion = document.getElementById("direccion").value;
    const celular = document.getElementById("celular").value;
    const correo = document.getElementById("correo").value;
    //const genero = document.getElementById("genero").value;
    const rol = document.getElementById("selectRoles").value;
    const empresa = document.getElementById("selectEmpresa").value;
    const puesto = document.getElementById("selectPuesto").value;
    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    if (nombres.length < 3) {
        alert("En nombres agregar más de tres carácteres");
        return;
    }
    if (apellidos.length < 3) {
        alert("En apellidos agregar más de tres carácteres");
        return;
    }

    if (isNaN(dpi) || dpi.length!=13) {
        alert(" Número de DPI incorrecto, ingresar 13 digitos");
        return;
    }

    if (isNaN(nit) || nit.length!=8) {
        alert("Número de NIT incorrecto, ingresar 8 digitos");
        return;
    }

    if (direccion.length < 5 ) {
        alert("En dirección agregar más de cinco carácteres");
        return;
    }

    if (isNaN(celular) || celular.length != 8) {
        alert("Número de celular incorrecto, ingresar 8 digitos");
        return;
    }

    if (!validarCorreo(correo)) {
        alert("Correo no válido");
        return;
    }
    if (isNaN(rol)) {
        alert("Por favor seleccionar rol");
        return;
    }
    if (isNaN(empresa)) {
        alert("Por favor seleccionar empresa");
        return;
    }
    
    if (isNaN(puesto)) {
        alert("Por favor seleccionar puesto");
        return;
    }
    if (isNaN(usuario) || isNaN(password)) {
        alert("Por favor ingresar usuario y contraseña");
        return;
    }
}

function add_empleado() {
    validarFormulario();
}

function mostrarEmpleados2() {
    pag_empl_empre++;
    get_empleados2();
}

function regresarEmpleados2() {
    if (pag_empl_empre > 1) {
        pag_empl_empre--;
        get_empleados2();
    }
}

// --------------------------------------------------------
// Funcion para obtener la lista de todos los empleados
// --------------------------------------------------------
function get_empleados2() {
    fetch('/empleados_empresa', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataEmpleado(data))
        .catch(error => console.log(error))
}


function get_puestos(tipo_select) {
    const type = tipo_select
    fetch('/puestos', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            json = data.puestos
            const select = document.getElementById(type);
            select.innerHTML = '';
            json.forEach(row => {
                const option = document.createElement('option');
                option.value = row.id;
                option.textContent = row.puesto;
                select.appendChild(option);
            }
            );
        })
        .catch(error => console.log(error))
}
// --------------------------------------------------------
// Funcion para mostrar nominas
// ---------------------------------------------------


function get_nominas() {
    fetch('/nominas', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataNominas(data))
        .catch(error => console.log(error))
}

function mostrarMasNomina() {
    pagina_nomina++;
    get_nominas();
}

function regresarNomina() {
    if (pagina_nomina > 1) {
        pagina_nomina--;
        get_nominas();
    }
}

function mostrarDataNominas(data) {
    data = data.nominas;
    let body = "";
    const inicio = (pagina_nomina - 1) * row_nomina;
    const fin = pagina_nomina * row_nomina;
    for (let i = inicio; i < fin; i++) {
        if (i < data.length) {
            body += `<tr>
                        <td>${data[i].id_empleado}</td>
                        <td>${data[i].nombre}</td>
                        <td>${data[i].nombre_rol}</td>
                        <td>${data[i].dias}</td>
                        <td>${data[i].sueldo}</td>
                        <td>${data[i].horas_extra}</td>
                        <td>${data[i].valor}</td>
                        <td>${data[i].comisiones}</td>
                        <td>${data[i].bonificaciones}</td>
                        <td>${data[i].TOTAL_DEVENGADO}</td>
                        <td>${data[i].IGGS}</td>
                        <td>${data[i].ISR}</td>
                        <td>${data[i].anticipo}</td>
                        <td>${data[i].descuento_prestamo}</td>
                        <td>${data[i].TotalDescuento}</td>
                        <td>${data[i].TOTAL_LIQUIDO}</td>
                        <td>
                            <button onclick="editar_nomina(${data[i].id_nomina})" class="btn btn-secondary"><ion-icon name="file-tray-full-outline"></ion-icon></button>
                        </td>
                    </tr>`;
        }
    }
    document.getElementById('data_nomina').innerHTML = body;
}


// --------------------------------------------------------
// Funcion para mostrar Prestamo
// ---------------------------------------------------



function get_prestamos() {
    fetch('/prestamos', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataPrestamos(data))
        .catch(error => console.log(error))
}

function mostrarDataPrestamos(data) {
    data = data.prestamos;
    let body = "";
    for (let i = 0; i < data.length; i++) {
        body += `<tr>
                    <td>${data[i].id_prestamo}</td>
                    <td>${data[i].id_usuario_solicita}</td>
                    <td>${data[i].fecha_atencion}</td>
                    <td>${data[i].descripcion}</td>
                    <td>${data[i].plazo_meses}</td>
                    <td>${data[i].pago_mensual}</td>
                    <td>${data[i].monto}</td>
                </tr>`;
    }
    document.getElementById('data_prestamos').innerHTML = body;
}


function add_prestamo() {
    const fecha_atencion = document.getElementById('fecha_atencion').value;
    const descripcion = document.getElementById('descripcion').value;
    const plazo_meses = document.getElementById('plazo_meses').value;
    const monto = document.getElementById('monto').value;
    const id_usuario_solicita = document.getElementById('id_usuario_solicita').value;
    const id_usuario_atiende = document.getElementById('id_usuario_atiende').value;

    if (!fecha_atencion || !descripcion || !plazo_meses || !monto || !id_usuario_solicita || !id_usuario_atiende) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    const body = {
        fecha_atencion,
        descripcion,
        plazo_meses,
        monto,
        id_usuario_solicita,
        id_usuario_atiende
    };

    const header = { "Content-Type": "application/json" };

    fetch('/insert_prestamo', {
        method: "POST",
        body: JSON.stringify(body),
        headers: header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            resetForm('insertar_prestamo'); 
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}


// --------------------------------------------------------
// Funcion para mostrar anticipo
// ---------------------------------------------------


function get_anticipos() {
    fetch('/anticipos', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataAnticipos(data))
        .catch(error => console.log(error))
}

function mostrarDataAnticipos(data) {
    data = data.anticipos;
    let body = "";
    for (let i = 0; i < data.length; i++) {
        body += `<tr>
                    <td>${data[i].id_anticipo}</td>
                    <td>${data[i].id_usuario}</td>
                    <td>${data[i].fecha_atencion}</td>
                    <td>${data[i].fecha_pago}</td>
                    <td>${data[i].descripcion}</td>
                    <td>${data[i].monto}</td>
                </tr>`;
    }
    document.getElementById('data_anticipo').innerHTML = body;
}

function add_anticipo() {
    const fecha_atencion = document.getElementById('fecha_atencion_anticipo').value;
    const fecha_pago = document.getElementById('fecha_pago').value;
    const descripcion = document.getElementById('descripcion_anticipo').value;
    const id_usuario = document.getElementById('id_usuario_anticipo').value;

    if (!fecha_atencion || !fecha_pago || !descripcion || !id_usuario) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    const body = {
        fecha_atencion,
        fecha_pago,
        descripcion,
        id_usuario
    };

    const header = { "Content-Type": "application/json" };

    fetch('/insert_anticipo', {
        method: "POST",
        body: JSON.stringify(body),
        headers: header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            resetForm('insertar_anticipo');
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}


// --------------------------------------------------------
// Funcion para mostrar nominass
// ---------------------------------------------------

function get_nominasss() {
    fetch('/nominass', { method: 'GET' })
        .then(response => response.json())
        .then(data => mostrarDataNominasss(data))
        .catch(error => console.log(error))
}


function mostrarMasNominass() {
    pagina_nominass++;
    get_nominass();
}

function regresarNominass() {
    if (pagina_nominass > 1) {
        pagina_nominass--;
        get_nominass();
    }
}

function mostrarDataNominasss(data) {
    data = data.nominas;
    let body = "";
    for (let i = 0; i < data.length; i++) {
        body += `<tr>
                    <td>${data[i].id_nomina}</td>
                    <td>${data[i].id_empleado}</td>
                    <td>${data[i].fecha}</td>
                    <td>${data[i].horas_trabajadas}</td>
                    <td>${data[i].horas_extra}</td>
                    <td>${data[i].ausencia_dias}</td>
                    <td>${data[i].dias}</td>
                    <td>${data[i].venta_total}</td>
                    <td>${data[i].comisiones}</td>
                    <td>${data[i].bonificaciones}</td>
                </tr>`;
    }
    document.getElementById('data_nominass').innerHTML = body;
}

function add_nomina() {
    const id_empleado = document.getElementById('id_empleado_nomina').value;
    const fecha = document.getElementById('fecha_nomina').value;
    const ausencia_dias = document.getElementById('ausencia_dias').value;
    const horas_extra = document.getElementById('horas_extra').value;
    const venta_total = document.getElementById('venta_total').value;


    if (!id_empleado || !fecha || !ausencia_dias || !horas_extra || !venta_total ) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    const body = {
        id_empleado,
        fecha,
        ausencia_dias,
        horas_extra,
        venta_total
    };

    const header = { "Content-Type": "application/json" };

    fetch('/insert_nomina', {
        method: "POST",
        body: JSON.stringify(body),
        headers: header
    })
        .then((res) => res.json())
        .then((response) => {
            alert(response.mensaje);
            resetForm('insertar_nomina'); 
            location.reload(true);
        })
        .catch((error) => console.error("Error", error))
}