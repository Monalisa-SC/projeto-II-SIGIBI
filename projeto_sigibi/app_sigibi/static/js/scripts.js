// scripts.js

// Exemplo 1: Mostrar alerta ao submeter formulário
document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmSubmit = confirm("Tem certeza que deseja enviar este formulário?");
            if (!confirmSubmit) {
                event.preventDefault(); // Evita o envio do formulário
            }
        });
    });
});

// Exemplo 2: Filtrar tabelas (adapte os IDs conforme necessário nos seus templates)
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let match = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].innerText.toUpperCase().includes(filter)) {
                match = true;
                break;
            }
        }
        rows[i].style.display = match ? "" : "none";
    }
}

// Exemplo 3: Atualizar contadores automaticamente (usado na página inicial)
function updateCounters() {
    const counters = document.querySelectorAll(".count");
    counters.forEach((counter) => {
        const target = parseInt(counter.innerText);
        let count = 0;
        const increment = Math.ceil(target / 100); // Incremento proporcional ao total
        const update = setInterval(() => {
            count += increment;
            if (count >= target) {
                count = target;
                clearInterval(update);
            }
            counter.innerText = count;
        }, 20);
    });
}

// Inicia contadores ao carregar a página (na página inicial)
document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector(".dashboard")) { // Verifica se estamos na página inicial
        updateCounters();
    }
});