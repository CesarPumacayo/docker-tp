// URL pública del backend desplegado en Render.
// Reemplazar por la URL real una vez creado el servicio en Render,
// por ejemplo: "https://docker-tp-backend.onrender.com"
const BACKEND_URL = "https://docker-tp-backend.onrender.com";

async function cargarUsuario() {
    const mensaje = document.getElementById("mensaje");

    try {
        const respuesta = await fetch(`${BACKEND_URL}/usuarios/1`);

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener el usuario");
        }

        const usuario = await respuesta.json();

        mensaje.textContent = `¡Bienvenido, ${usuario.nombre}!`;

    } catch (error) {
        console.error(error);
        mensaje.textContent = "Error al cargar el usuario";
    }
}

cargarUsuario();