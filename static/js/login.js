const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const password_regex = /^.{8,64}$/;


document
    .getElementById("register-form")
    .addEventListener("submit", async (_) => {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const error_el = document.getElementById("error");

        if (!username_regex.test(username)) {
            error_el.textContent = "Invalid username";
            return;
        }

        if (!password_regex.test(password)) {
            error_el.textContent = "Invalid password, must be at least 8 characters";
            return;
        }

        try {
            const response = await fetch("api/v1/auth/login", {
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
                    error_el.textContent = "Something went wrong. Please try again later!";
                    break;
            }
        }
        catch (error) {
            console.log(error);
            error_el.textContent = "Something went wrong. Please try again later!";
        }
    });