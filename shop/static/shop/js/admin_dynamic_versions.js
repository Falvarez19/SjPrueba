document.addEventListener("DOMContentLoaded", function () {
    const modelField = document.querySelector("#id_model");
    let versionField = document.querySelector("#id_version");

    // Datos de versiones precargadas en JSON desde Django
    let versionsData = {};
    const versionsDataElement = document.getElementById("versions-data");
    if (versionsDataElement) {
        versionsData = JSON.parse(versionsDataElement.textContent);
    }

    // Opciones de versiones por modelo si no hay JSON dinámico
    const versionesPorModelo = {
        "ONIX": ["FULL", "1.2", "LTC"],
        "TRACKER": ["LT", "LTZ", "PREMIER"],
        "S10": ["LS", "LT", "HIGH COUNTRY"],
        "MONTANA": ["BASE", "PREMIUM"],
        "SPIN": ["LT", "LTZ"]
    };

    function actualizarVersiones() {
        const modeloSeleccionado = modelField.value;

        // Verificar si el campo versión ya es un <select>, si no, crearlo
        if (!(versionField.tagName.toLowerCase() === "select")) {
            const nuevoSelect = document.createElement("select");
            nuevoSelect.id = "id_version";
            nuevoSelect.name = "version";
            nuevoSelect.classList = versionField.classList;
            versionField.replaceWith(nuevoSelect);
            versionField = nuevoSelect;
        }

        versionField.innerHTML = ""; // Limpiar opciones previas

        // Agregar opción por defecto
        let defaultOption = new Option("Seleccione una versión", "");
        versionField.appendChild(defaultOption);

        // Primero intenta cargar desde JSON precargado, luego desde la API
        let versiones = versionsData[modeloSeleccionado] || versionesPorModelo[modeloSeleccionado];

        if (versiones) {
            versiones.forEach(version => {
                let option = new Option(version.name || version, version.id || version);
                versionField.appendChild(option);
            });
        } else {
            // Si no hay datos en el JSON, intenta cargar desde la API
            fetch(`/api/get_versions/${modeloSeleccionado}/`)
                .then(response => response.json())
                .then(data => {
                    versionField.innerHTML = "";
                    let defaultOption = new Option("Seleccione una versión", "");
                    versionField.appendChild(defaultOption);

                    data.versions.forEach(version => {
                        let option = new Option(version.name, version.id);
                        versionField.appendChild(option);
                    });
                })
                .catch(error => console.error("Error cargando versiones desde API:", error));
        }
    }

    // Detectar cambio en el modelo
    modelField.addEventListener("change", actualizarVersiones);

    // Ejecutar la función al cargar la página si hay un modelo seleccionado
    actualizarVersiones();
});
