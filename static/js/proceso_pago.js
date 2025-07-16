// --------------------
// Variables y helpers
// --------------------

// Controla el paso actual del proceso de pago (1: Envío, 2: Entrega, 3: Pago)
let currentStep = 1;

// --------------------
// Validación de pasos
// --------------------

/**
 * Valida los campos del paso actual del formulario y muestra el siguiente paso si todo está OK.
 * @param {number} paso - Paso actual (1 o 2)
 */
function validarPaso(paso) {
    limpiarErrores();
    let valid = true;

    if (paso === 1) {
        // Lista de campos obligatorios a validar en el paso 1
        const fields = [
            { id: 'id_direccion', errorId: 'direccion-error', message: 'La dirección es requerida' },
            { id: 'id_nombre', errorId: 'nombre-error', message: 'El nombre es requerido' },
            { id: 'id_apellidos', errorId: 'apellidos-error', message: 'Los apellidos son requeridos' },
            { id: 'id_email', errorId: 'email-error', message: 'El correo electrónico es requerido' }
        ];

        // Validación de campos vacíos
        fields.forEach(field => {
            const input = document.getElementById(field.id);
            if (!input.value.trim()) {
                document.getElementById(field.errorId).textContent = field.message;
                valid = false;
            }
        });

        // Validación de formato de email
        const email = document.getElementById("id_email");
        const emailValue = email.value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailValue)) {
            document.getElementById("email-error").textContent = 'Ingrese un correo electrónico válido';
            valid = false;
        }

        // Validación de teléfono (9 dígitos, formato chileno)
        const telefono = document.getElementById("id_telefono");
        const telefonoValue = telefono.value.replace(/\s/g, '');
        if (telefonoValue.length !== 9) {
            document.getElementById("telefono-error").textContent = 'Debe tener 9 dígitos en formato X XXXXXXXX';
            valid = false;
        }

        // Validación de RUT (8 o 9 dígitos, sin guión)
        const rut = document.getElementById("id_rut");
        const rutValue = rut.value.replace(/\D/g, '');
        if (rutValue.length < 8 || rutValue.length > 9) {
            document.getElementById("rut-error").textContent = 'Debe tener entre 8 y 9 dígitos sin guiones';
            valid = false;
        }

        // Validación de aceptación de términos
        const terminos = document.getElementById("id_terminos");
        if (!terminos.checked) {
            document.getElementById("terminos-error").textContent = 'Debes aceptar los términos y condiciones.';
            valid = false;
        }

        // Si todo está correcto, muestra el paso 2
        if (valid) mostrarPaso(2);

    } else if (paso === 2) {
        // Paso 2 no tiene validaciones adicionales, solo avanza
        mostrarPaso(3);
    }
}

/**
 * Valida los campos del paso 3 (datos de la tarjeta) al intentar enviar el formulario.
 * @returns {boolean} - Si la validación es exitosa
 */
function validarPaso3() {
    limpiarErrores();
    let valid = true;

    const numeroTarjeta = document.getElementById('id_numero_tarjeta');
    const fechaVencimiento = document.getElementById('id_fecha_vencimiento');
    const codigoSeguridad = document.getElementById('id_codigo_seguridad');

    // Validación de número de tarjeta (16 dígitos)
    if (numeroTarjeta.value.replace(/\s/g, '').length !== 16) {
        document.getElementById('numero_tarjeta-error').textContent = 'Debe tener 16 dígitos en formato XXXX XXXX XXXX XXXX';
        valid = false;
    }

    // Validación de fecha de vencimiento (MM/AA)
    if (!/^\d{2}\/\d{2}$/.test(fechaVencimiento.value)) {
        document.getElementById('fecha_vencimiento-error').textContent = 'Formato inválido, debe ser MM/AA';
        valid = false;
    }

    // Validación de CVV (3 dígitos)
    if (codigoSeguridad.value.length !== 3) {
        document.getElementById('codigo_seguridad-error').textContent = 'El CVV debe tener 3 dígitos';
        valid = false;
    }

    return valid;
}

// --------------------
// Funciones utilitarias
// --------------------

/**
 * Limpia todos los mensajes de error en el formulario.
 */
function limpiarErrores() {
    document.querySelectorAll('.text-danger').forEach(el => el.textContent = '');
}

/**
 * Muestra solo el paso indicado y oculta los otros.
 * @param {number} paso - Paso a mostrar (1, 2 o 3)
 */
function mostrarPaso(paso) {
    currentStep = paso;
    document.getElementById('paso1').style.display = paso === 1 ? 'block' : 'none';
    document.getElementById('paso2').style.display = paso === 2 ? 'block' : 'none';
    document.getElementById('paso3').style.display = paso === 3 ? 'block' : 'none';
}

// --------------------
// Formateo y restricción de campos en tiempo real
// --------------------

// Al cargar la página, muestra el paso actual
document.addEventListener("DOMContentLoaded", function() {
    mostrarPaso(currentStep);
});

// Formatea el número de tarjeta a XXXX XXXX XXXX XXXX
document.getElementById('id_numero_tarjeta').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 16);
    e.target.value = value.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
});

// Permite solo números en RUT, máximo 9 dígitos
document.getElementById('id_rut').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 9);
    e.target.value = value;
});

// Permite solo números en teléfono, máximo 9 dígitos, formato X XXXXXXXX
document.getElementById('id_telefono').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 9);
    if (value.length > 1) value = value[0] + ' ' + value.slice(1);
    e.target.value = value;
});

// Permite solo letras y espacios en nombres y apellidos
document.getElementById('id_nombre').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});
document.getElementById('id_apellidos').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});

// Formatea la fecha de vencimiento como MM/AA
document.getElementById('id_fecha_vencimiento').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 4);
    if (value.length >= 2) e.target.value = value.slice(0, 2) + '/' + value.slice(2);
    else e.target.value = value;
});

// Permite solo 3 dígitos en el CVV
document.getElementById('id_codigo_seguridad').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 3);
    e.target.value = value;
});
