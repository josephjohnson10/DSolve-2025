const API_URL = "http://127.0.0.1:5000";

function showRegister() {
    document.getElementById("auth").style.display = "none";
    document.getElementById("register").style.display = "block";
}

function showLogin() {
    console.log('hiii')
    document.getElementById("auth").style.display = "block";
    document.getElementById("register").style.display = "none";
}

function register() {
    const name = document.getElementById("regName").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;

    fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
    }).then(res => res.json()).then(data => {
        alert(data.message);
        showLogin();
    });
}

function login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    }).then(res => res.json()).then(data => {
        if (data.user) {
            localStorage.setItem("user", JSON.stringify(data.user));
            window.location.href = "/dashboard";
            console.log("login success")
        } else {
            alert(data.error);
        }
    });
}
