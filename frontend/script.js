// URL pública del backend desplegado en Render.
// Reemplazar por la URL real que muestra el panel de Render.
// En local (localhost) se usa /api, que nginx redirige al backend.
const BACKEND_URL =
    location.hostname === "localhost"
        ? "/api"
        : "https://docker-tp.onrender.com";

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