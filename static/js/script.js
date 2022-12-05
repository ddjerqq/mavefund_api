async function login(e) {
    e.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    const response = await fetch("https://127.0.0.1:443/auth/login", {
        method: 'POST',
        headers: new Headers({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify({
            "username": username,
            "password": password
        }),
        redirect: 'follow'
    });

    const data = await response.json();

    if (response.status === 200) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("username", username);
        window.location.replace("index.html");
    }
    else {
        alert(`Error ${data.status}`);
    }
}


async function register(e) {
    e.preventDefault();

    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    const response = await fetch("https://127.0.0.1:443/auth/register", {
        method: "POST",
        headers: new Headers({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify({
            "username": username,
            "email": email,
            "password": password
        }),
        redirect: "follow"
    });

    const data = await response.json();

    if (response.status === 200) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("username", username);
        window.location.replace("index.html");
    }
    else {
        alert(`Error ${data.status}`);
    }
}
