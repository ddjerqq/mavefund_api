async function login(_) {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const error_el = document.getElementById("error");

    const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
    // password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const password_regex = /^.{8,64}$/;

    if (!username_regex.test(username)) {
        error_el.textContent = "Invalid username";
        return;
    }

    if (!password_regex.test(password)) {
        error_el.textContent = "Invalid password, must be at least 8 characters";
        return;
    }

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: new Headers({
                "content-type": "application/json"
            }),
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "password": password
            }),
        });

        switch (response.status) {
            case 200:
                const token = await response.json();
                localStorage.setItem("token", token);
                localStorage.setItem("username", username);

                document.cookie = `token=${token}`;

                window.location.replace("/");
                break;

            case 404:
                error_el.textContent = "Username is not registered, please register";
                break;

            case 400:
                error_el.textContent = "Password is incorrect";
                break;

            default:
                let err = await response.json();
                error_el.textContent = `Something went wrong. ${err.detail}`;
                break;
        }
    }
    catch (error) {
        console.log(error);
        error_el.textContent = "Something went wrong. Please try again later!";
    }
}

async function register(_) {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const repeat_password = document.getElementById("repeat_password").value;
    const error_el = document.getElementById("error");

    const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
    const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,255}$/;
    // password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,64}$/;

    if (!username_regex.test(username)) {
        error_el.textContent = "Invalid username";
        return;
    }

    if (!email_regex.test(email)) {
        error_el.textContent = "Invalid email";
        return;
    }

    if (!password_regex.test(password)) {
        error_el.textContent = "Invalid password, must be at least 8 characters, 1 uppercase, 1 lowercase, 1 number";
        return;
    }

    if (password !== repeat_password) {
        error_el.textContent = "Passwords do not match";
        return;
    }

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
               "content-type": "application/json"
            },
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "email": email,
                "password": password,
            }),
        });

        let detail = null;

        switch (response.status) {
            case 200:
                const token = await response.json();
                localStorage.setItem("token", token);
                localStorage.setItem("username", username);

                document.cookie = `token=${token}`;

                // redirect to index.
                window.location.replace("/");
                break;

            case 409:
                detail = await response.json();
                if (detail.includes("username")) {
                    error_el.textContent = "Username is already registered";
                }
                else if (detail.includes("email")) {
                    error_el.textContent = "Email is already registered";
                }
                else {
                    error_el.textContent = `Something went wrong. ${detail}`;
                }
                break;

            default:
                detail = await response.json();
                error_el.textContent = `Something went wrong. ${detail}`;
                break;
        }

    } catch (error) {
        console.log(error);
        error_el.textContent = `Something went wrong.`;
    }
}


// todo make searchbar work
async function submit(e) {
    console.log(e);
    e.preventDefault();

    let ticker = document.getElementById("ticker").value;

    if (ticker === "") {
        alert("Please fill in all fields");
        return;
    }

    alert(`you are searching for ${ticker}`);
}
