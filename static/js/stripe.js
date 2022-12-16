const BASIC_PRICE_ID = "price_1MFS3GLGZqgNQZ5xSM08eOPt";
const PREMIUM_PRICE_ID = "price_1MFS4MLGZqgNQZ5x104ipW9N";
const SUPER_PRICE_ID = "price_1MFS5ILGZqgNQZ5xW3GEw2F3";


async function createCheckoutSession(priceId) {
    const response = await fetch("/api/v1/stripe/create_checkout_session", {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify({
            priceId: priceId,
        }),
    });

    return await response.json();
}


document
    .addEventListener("DOMContentLoaded", () => {
        document
            .getElementById("checkout-basic")
            .addEventListener("click", async () => {
                let session = await createCheckoutSession(BASIC_PRICE_ID);
                if (session.status === "success") {
                    window.location.href = session.url;
                } else {
                    console.log(session.error);
                    alert(session.message);
                }
            });

        document
            .getElementById("checkout-premium")
            .addEventListener("click", async () => {
                let session = await createCheckoutSession(PREMIUM_PRICE_ID);
                if (session.status === "success") {
                    window.location.href = session.url;
                } else {
                    console.log(session.error);
                    alert(session.message);
                }
            });

        document
            .getElementById("checkout-super")
            .addEventListener("click", async () => {
                let session = await createCheckoutSession(SUPER_PRICE_ID);
                if (session.status === "success") {
                    window.location.href = session.url;
                } else {
                    console.log(session.error);
                    alert(session.message);
                }
            });
    })
