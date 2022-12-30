import os
import stripe
from fastapi import APIRouter, Request, Header, Depends

from starlette.responses import RedirectResponse

from src.dependencies.auth import authenticated_only
from src.data import ApplicationDbContext


class StripeRouter:
    PRICE_ID_TO_RANK = {
        os.getenv("BASIC_SUBSCRIPTION_PRICE_ID"): 0,
        os.getenv("PREMIUM_SUBSCRIPTION_PRICE_ID"): 1,
        os.getenv("SUPER_SUBSCRIPTION_PRICE_ID"): 2,
    }

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/stripe",
        )

        self.router.add_api_route(
            "/create_checkout_session",
            self.create_checkout_session,
            methods=["POST"],
            description="create a checkout session",
        )

        self.router.add_api_route(
            "/create_portal_session",
            self.create_portal_session,
            methods=["POST"],
            description="create a portal session",
            dependencies=[Depends(authenticated_only)],
        )

        self.router.add_api_route(
            "/success",
            self.success,
            methods=["GET"],
            description="success page",
        )

        self.router.add_api_route(
            "/cancel",
            self.cancel,
            methods=["GET"],
            description="cancel page",
        )

        self.router.add_api_route(
            "/webhook",
            self.webhook,
            methods=["POST"],
            description="Stripe Webhook",
        )

    async def create_checkout_session(self, req: Request) -> dict:
        print(self.PRICE_ID_TO_RANK)

        if req.user is None:
            return {"status": "fail", "message": "Please log in or register before subscribing."}

        data = await req.json()
        price_id = data["priceId"]

        # 0 - basic, 1 - premium, 2 - super
        if req.user.rank >= self.PRICE_ID_TO_RANK[price_id]:
            return {"status": "fail", "message": "User is already subscribed!"}

        checkout_session = stripe.checkout.Session.create(
            client_reference_id=req.user.id,
            metadata={"rank": self.PRICE_ID_TO_RANK[price_id]},
            success_url="https://mavefund.com/api/v1/stripe/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://mavefund.com/api/v1/stripe/cancel",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }]
        )
        return {
            "status": "success",
            "id": checkout_session["id"],
            "url": checkout_session["url"]
        }

    async def create_portal_session(self, req: Request):
        session = stripe.billing_portal.Session.create(
            customer=req.user.id,
            return_url="/"
        )
        return {
            "url": session.url
        }

    async def success(self, req: Request, session_id: str) -> RedirectResponse:

        session = stripe.checkout.Session.retrieve(session_id)

        if session["payment_status"] == "paid":
            rank = int(session["metadata"]["rank"])
            user_id = int(session["client_reference_id"])
            user = await self.db.users.get_by_id(user_id)
            user.rank = rank
            await self.db.users.update(user)

        return RedirectResponse(url="/")  # TODO redirect to dashboard

    async def cancel(self, req: Request) -> RedirectResponse:
        return RedirectResponse(url="/")  # TODO redirect to dashboard

    async def webhook(
            self,
            req: Request,
            stripe_signature: str = Header(str)
    ) -> dict:
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        data = await req.body()

        try:
            event = stripe.Webhook.construct_event(
                payload=data,
                sig_header=stripe_signature,
                secret=webhook_secret
            )
            event_data = event["data"]
            print(event)
        except Exception as e:
            print(e)
            return {"error": str(e)}


        if event["type"] == "checkout.session.completed":
            session = event_data["object"]
            metadata = session.get("metadata")
            if metadata is not None and "rank" in metadata:
                rank = int(metadata["rank"])
                client_reference_id = session.get(
                    "client_reference_id"  # user id
                )
                user = await self.db.users.get_by_id(int(client_reference_id))
                user.rank = rank
                await self.db.users.update(user)
            return {"status": "success"}

        elif event["type"] == "invoice.paid":
            print("invoice.paid")
            # print(event_data)

        elif event["type"] == "invoice.payment_failed":
            print("invoice.payment_failed")
            # print(event_data)
            return {"status": "fail", "message": "payment failed"}

        else:
            print("Unhandled event type")
            # print(event_data)

        return {"status": "success"}
