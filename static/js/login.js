const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const login_password_regex = /^.{8,64}$/;
const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,255}$/;
// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const register_password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,64}$/;

const container = document.getElementById("container");


document
    .getElementById("sign-up")
    .addEventListener("click", () => {
        container.classList.add("right-panel-active");
    });

document
    .getElementById("sign-in")
    .addEventListener("click", () => {
        container.classList.remove("right-panel-active");
    });


async function register() {

    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const error_el = document.getElementById("register-error");
    const recaptcha_token = document.getElementById("register-captcha").value;

    if (!username_regex.test(username)) {
        error_el.textContent = "Invalid username";
        return;
    }

    if (!email_regex.test(email)) {
        error_el.textContent = "Invalid email";
        return;
    }

    if (!register_password_regex.test(password)) {
        error_el.textContent = "Invalid password, must be at least 8 characters, 1 uppercase, 1 lowercase, 1 number";
        return;
    }

    let response;

    try {
        response = await fetch("api/v1/auth/register", {
            method: "POST",
            headers: {
                "content-type": "application/json"
            },
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "email": email,
                "password": password,
                "recaptcha_token": recaptcha_token
            }),
        });
    } catch (error) {
        console.log(error);
        error_el.textContent = "Something went wrong. Please try again later!";
        return;
    }

    let detail = null;

    switch (response.status) {
        case 200:
            const message = await response.json();
            alert(message)
            window.location.replace("/");
            break;

        case 409:
            detail = await response.json();
            if (detail.includes("username")) {
                error_el.textContent = "Username is already registered";
            } else if (detail.includes("email")) {
                error_el.textContent = "Email is already registered";
            } else {
                error_el.textContent = "Email or username already taken.";
            }
            break;
        case 400:
            detail = await response.json();
            error_el.textContent = detail;
            break;

        default:
            error_el.textContent = "Something went wrong. Please try again later!";
            break;
    }
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const error_el = document.getElementById("login-error");
    const recaptcha_token = document.getElementById("login-captcha").value;

    if (!username_regex.test(username)) {
        error_el.textContent = "Invalid username";
        return;
    }

    if (!login_password_regex.test(password)) {
        error_el.textContent = "Invalid password, must be at least 8 characters";
        return;
    }

    let response;

    try {
        response = await fetch("api/v1/auth/login", {
            method: "POST",
            headers: new Headers({
                "content-type": "application/json"
            }),
            redirect: "follow",
            body: JSON.stringify({
                "username": username,
                "password": password,
                "recaptcha_token": recaptcha_token
            }),
        });
    } catch (error) {
        console.log(error);
        error_el.textContent = "Something went wrong. Please try again later!";
        return
    }

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
        case 403:
            error_el.textContent = "Please verify your email address!";
            break;

        case 400:
            const message = await response.json()
            if (message.detail === 'unverified') {
                error_el.textContent = "Please verify your email address!"
            } else {
                error_el.textContent = "Password is incorrect";
            }
            break;

        default:
            error_el.textContent = "Something went wrong. Please try again later!";
            break;
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("login-form").addEventListener("submit", function (e) {
        e.preventDefault() // Cancel the default action
        return login();
    });

    document.getElementById("register-form").addEventListener("submit", function (e) {
        e.preventDefault() // Cancel the default action
        return register();
    });

    let params = (new URL(document.location)).searchParams;
    let message = params.get("m");
    let login_info = document.getElementById('login-info')
    if (message === 'password-reset') {
        login_info.textContent = "your password has been changed successfully!"
    } else if (message === 'email-verified') {
        login_info.textContent = "your email has been verified successfully!"
    }
});