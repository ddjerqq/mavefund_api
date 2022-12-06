async function login(e) {
    e.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: new Headers({
                "Content-Type": "application/json"
            }),
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "password": password
            }),
        });

        if (response.status === 200) {
            const token = await response.json();
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);

            document.cookie = `token=${token}`;

            window.location.replace("/");
        }
        else {
            alert(`Error`);
        }
    }
    catch (error) {
        console.log(error);
    }
}


async function register(e) {
    e.preventDefault();

    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (username === "" || email === "" || password === "") {
        alert("Please fill in all fields");
        return;
    }

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
               "Content-Type": "application/json"
            },
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "email": email,
                "password": password,
            }),
        });

        if (response.status === 200) {
            const token = await response.json();
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);

            document.cookie = `token=${token}`;

            // redirect to index.
            window.location.replace("/");
        }
        else {
            alert(`Error`);
        }

    } catch (error) {
        console.log(error);
    }
}
