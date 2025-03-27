const API_URL = "http://127.0.0.1:5000";

function addItem() {
    console.log('in func')
    const name = document.getElementById("itemName").value;
    const location = document.getElementById("itemLocation").value;
    const status = document.getElementById("itemStatus").value;

    console.log(name,location,status)
    fetch(`${API_URL}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, location, status }),
    }).then(res => res.json()).then(data => {
        alert(data.message);
        fetchItems(); // Refresh items list
    }).catch(err => console.error("Error:", err));
}

function fetchItems() {
    fetch(`${API_URL}/items`)
    .then(res => res.json())
    .then(items => {
        const list = document.getElementById("itemsList");
        list.innerHTML = ""; // Clear previous list

        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.name} - ${item.location}`;
            list.appendChild(li);
        });
    }).catch(err => console.error("Error:", err));
}

// Load items on page load
document.addEventListener("DOMContentLoaded", fetchItems);
