const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,255}$/;

// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,64}$/;

document
    .getElementById("register-form")
    .addEventListener("submit", async (_) => {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const repeat_password = document.getElementById("repeat_password").value;
        const error_el = document.getElementById("error");

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
            const response = await fetch("api/v1/auth/register", {
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
                    error_el.textContent = "Something went wrong. Please try again later!";
                    break;
            }

        } catch (error) {
            console.log(error);
            error_el.textContent = "Something went wrong. Please try again later!";
        }
    });