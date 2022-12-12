import os
import stripe
from fastapi import APIRouter, Request, Header, Depends

from src.dependencies.auth import authenticated_only
from src.data import ApplicationDbContext


class StripeRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/stripe",
            dependencies=[Depends(authenticated_only)],
        )

        self.router.add_api_route(
            "/create_checkout_session",
            self.create_checkout_session,
            methods=["POST"],
            description="create a checkout session"
        )

        self.router.add_api_route(
            "/create_portal_session",
            self.create_portal_session,
            methods=["POST"],
            description="create a portal session"
        )


    async def create_checkout_session(self, req: Request):
        data = await req.json()

        checkout_session = stripe.checkout.Session.create(
            customer=req.user.id,
            success_url=f"api/v1/stripe/success?session_id={{CHECKOUT_SESSION_ID}}&user_id={req.user.id}",
            cancel_url="api/v1/stripe/cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": data["price_id"],
                "quantity": 1,
            }]
        )
        return {"id": checkout_session["id"]}


    async def create_portal_session(self, req: Request):
        session = stripe.billing_portal.Session.create(
            customer=req.user.id,
            return_url="/"
        )
        return {"url": session.url}


    async def success(self, req: Request, session_id: str, user_id: str):
        print(f"success called with session_id: {session_id}")
        print(f"success called with user_id: {user_id}")
        return {"message": "success called"}


    async def cancel(self, req: Request):
        print("cancel called")
        return {"message": "cancel called"}


    async def webhook_received(self, req: Request, stripe_signature: str = Header(str)):
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        data = await req.body()
        try:
            event = stripe.Webhook.construct_event(
                payload=data,
                sig_header=stripe_signature,
                secret=webhook_secret
            )
            event_data = event["data"]
        except Exception as e:
            return {"error": str(e)}

        if event["type"] == "checkout.session.completed":
            print("checkout.session.completed")
            print(event_data)

        elif event["type"] == "invoice.paid":
            print("invoice.paid")
            print(event_data)

        elif event["type"] == "invoice.payment_failed":
            print("invoice.payment_failed")
            print(event_data)
        else:
            print("Unhandled event type")
            print(event_data)

        return {"status": "success"}
