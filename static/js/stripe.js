const BASIC_PRICE_ID = "price_1MDUQrLGZqgNQZ5xlffZbFP8";
const PREMIUM_PRICE_ID = "price_1MDUQ6LGZqgNQZ5xVSB30Byw";
const SUPER_PRICE_ID = "price_1MDUOMLGZqgNQZ5xnDIliHKM";


const stripe = Stripe("pk_test_51MClgyLGZqgNQZ5xQeSSLOkrHtrhYRDQTe7jCyx9ZeVdCVPOb75mQ79SBeKA1GCjCI9Ip9HLbw6Q6OR5TQfNmNUK00J9Kz4qAu");


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
                let session = createCheckoutSession(BASIC_PRICE_ID);
                stripe.redirectToCheckout({ sessionId: session.id });
            });

        document
            .getElementById("checkout-premium")
            .addEventListener("click", async () => {
                let session = createCheckoutSession(PREMIUM_PRICE_ID);
                stripe.redirectToCheckout({ sessionId: session.id });
            });

        document
            .getElementById("checkout-super")
            .addEventListener("click", async () => {
                let session = createCheckoutSession(SUPER_PRICE_ID);
                stripe.redirectToCheckout({ sessionId: session.id });
            });
    })
