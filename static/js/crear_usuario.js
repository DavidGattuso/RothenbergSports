//crear_usuario.html

// Validación de formato de teléfono en tiempo real
document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '').slice(0, 9);
    if (value.length > 1) {
        value = value[0] + ' ' + value.slice(1);
    }
    e.target.value = value;
});

// Validación de formato de fecha de nacimiento en tiempo real
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

// Restringir caracteres en el campo de nombre a letras y espacios
document.getElementById('first_name').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});

// Restringir caracteres en el campo de apellido a letras y espacios
document.getElementById('last_name').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^a-zA-Z\s]/g, '');
});