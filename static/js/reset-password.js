// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const login_password_regex = /^.{8,64}$/;

async function submit_form() {
    const password = document.getElementById('password').value;
    const token = document.getElementById('token').value;
    const error_el = document.getElementById("reset-error");
    if (!login_password_regex.test(password)) {
        error_el.textContent = "Invalid password";
        return;
    }

    try {
        var response = await fetch("/api/v1/auth/reset-password-verify", {
            method: "POST",
            headers: new Headers({
                "content-type": "application/json"
            }),
            redirect: "follow",
            body: JSON.stringify({
                "password": password,
                "token": token,
            }),
        });
    } catch (error) {
        console.log(error);
        error_el.textContent = "Something went wrong. Please try again later!";
    }

    switch (response.status) {
        case 200:
            alert("your password has been changed successfully")
            // redirect to index.
            window.location.replace("/login?m=password-reset");
            break;

        case 400:
            error_el.textContent = "Invalid Token";
            break;


        default:
            error_el.textContent = "Something went wrong. Please try again later!";
            break;
    }
}


document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("reset-form").addEventListener("submit", function (e) {
        e.preventDefault() // Cancel the default action
        return submit_form();
    });
});