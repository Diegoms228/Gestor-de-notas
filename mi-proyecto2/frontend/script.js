const API_URL = "http://localhost:5000/api";

// ── LOGIN ──────────────────────────────────────────────────────────────────
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("usuario").value.trim();
        const password = document.getElementById("password").value;
        const errorMsg = document.getElementById("error-msg");

        errorMsg.textContent = "";

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                errorMsg.textContent = data.error || "Error al iniciar sesión";
                return;
            }

            // Guardar token y redirigir
            localStorage.setItem("token", data.token);
            localStorage.setItem("username", data.username);
            window.location.href = "notas.html";

        } catch (error) {
            errorMsg.textContent = "No se pudo conectar con el servidor";
        }
    });
}

// ── REGISTRO ───────────────────────────────────────────────────────────────
const registroForm = document.getElementById("registroForm");
if (registroForm) {
    registroForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const nombre    = document.getElementById("nombre").value.trim();
        const apellidos = document.getElementById("apellidos").value.trim();
        const email     = document.getElementById("email").value.trim();
        const username  = document.getElementById("usuario").value.trim();
        const password  = document.getElementById("password").value;
        const errorMsg  = document.getElementById("error-msg");

        errorMsg.textContent = "";

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nombre, apellidos, email, username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                errorMsg.textContent = data.error || "Error al registrarse";
                return;
            }

            // Registro OK → ir al login
            window.location.href = "index.html";

        } catch (error) {
            errorMsg.textContent = "No se pudo conectar con el servidor";
        }
    });
}
