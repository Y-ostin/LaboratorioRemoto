// Funcion para mostrar notificacion flotante
function mostrarNotificacion(mensaje, exito = true) {
    const toastEl = document.getElementById("toast");
    const toastBody = document.getElementById("toast-body");

    toastBody.textContent = mensaje;
    toastEl.classList.remove("text-bg-success", "text-bg-danger");
    toastEl.classList.add(exito ? "text-bg-success" : "text-bg-danger");

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// Funcion para manejar el envio de formularios
async function enviarFormulario(formularioId, url) {
    const form = document.getElementById(formularioId);
    const formData = new FormData(form);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: new URLSearchParams(formData)
        });
        console.log(response);

        if (response.ok) {
            mostrarNotificacion("Datos enviados correctamente.", true);
        } else {
            mostrarNotificacion("Error al enviar datos.", false);
        }
    } catch (error) {
        console.error("error de conexion", error);
        mostrarNotificacion("Error de conexion.", false);
    }
}

// Manejadores de eventos para formularios
document.getElementById("formAltura").addEventListener("submit", (event) => {
    event.preventDefault();
    enviarFormulario("formAltura", "/set_altura");
});

document.getElementById("formPID").addEventListener("submit", (event) => {
    event.preventDefault();
    enviarFormulario("formPID", "/set_pid");
});
