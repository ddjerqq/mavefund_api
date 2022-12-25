const username_regex = /^[a-zA-Z0-9._]{3,32}$/;
// password regex with at least 8 characters, 1 uppercase, 1 lowercase, 1 number
const login_password_regex = /^.{8,64}$/;
const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,255}$/;

async function submit_form() {
    const email = document.getElementById("email").value;
    const error_el = document.getElementById("reset-error");
    if (!email_regex.test(email)) {
        error_el.textContent = "Invalid email";
        return;
    }

    try {
        var response = await fetch("/api/v1/auth/reset-password", {
            method: "POST",
            headers: new Headers({
                "content-type": "application/json"
            }),
            redirect: "follow",
            body: JSON.stringify({
                "email": email,
            }),
        });
    } catch (error) {
        console.log(error);
        error_el.textContent = "Something went wrong. Please try again later!";
    }

    switch (response.status) {
        case 200:
            const message = await response.json();
            alert(message)
            break;

        case 400:
            error_el.textContent = "There's no account associated with this email address!";
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