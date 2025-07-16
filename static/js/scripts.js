// Cambia el año del footer automaticamente (base.html)
document.addEventListener("DOMContentLoaded", function() {
    var yearSpan = document.getElementById("year");
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});

// Script para cierre automático de alertas (base.html)
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alert = document.querySelector(".alert");
        if (alert) {
            alert.classList.add("fade");
            alert.addEventListener("transitionend", () => alert.remove());
        }
    }, 5000);
});


// Valida formularios Bootstrap 5 en toda la web: evita envío si hay campos inválidos.
// Aplica a cualquier form con la clase "needs-validation".
// actualizar_perfil.html - login.html
(function () {
    'use strict';
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();


// Validación de formato de teléfono en tiempo real (register.html)
document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 9); 
    if (value.length > 1) {
        value = value[0] + ' ' + value.slice(1); 
    }
    e.target.value = value;
});


// Validación de formato de fecha de nacimiento en tiempo real (register.html)
document.getElementById('birth_date').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 8);
    let formatted = '';
    if (value.length > 2) {
        formatted = value.slice(0, 2) + '/';
        if (value.length > 4) {
            formatted += value.slice(2, 4) + '/';
            formatted += value.slice(4, 8);
        } else {
            formatted += value.slice(2);
        }
    } else {
        formatted = value;
    }
    e.target.value = formatted;
});


// Restringir caracteres en el campo de nombre a letras y espacios (register.html)
document.getElementById('first_name').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});


// Restringir caracteres en el campo de apellido a letras y espacios (register.html)
document.getElementById('last_name').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});