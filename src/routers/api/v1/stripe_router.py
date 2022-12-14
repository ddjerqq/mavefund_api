import os
import stripe
from fastapi import APIRouter, Request, Header, Depends

from src.dependencies.auth import authenticated_only
from src.data import ApplicationDbContext

SUPER_SUBSCRIPTION_ID = os.getenv('SUPER_SUBSCRIPTION_ID')
PREMIUM_SUBSCRIPTION_ID = os.getenv('PREMIUM_SUBSCRIPTION_ID')
BASIC_SUBSCRIPTION_ID = os.getenv('BASIC_SUBSCRIPTION_ID')
DOMAIN_URL = os.getenv('DOMAIN_URL')
PRICE_TO_RANK = {
    SUPER_SUBSCRIPTION_ID: 2,
    PREMIUM_SUBSCRIPTION_ID: 1,
    BASIC_SUBSCRIPTION_ID: 0,
}


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
        if req.user.rank in [0, 1, 2, 3]:
            return {'message': "User is already subscribed!", 'success': False}
        data = await req.json()
        price = data["priceId"]
        rank = PRICE_TO_RANK[price]
        metadata = {'rank': rank}

        checkout_session = stripe.checkout.Session.create(
            client_reference_id=req.user.id,
            metadata=metadata,
            success_url=f"{DOMAIN_URL}/api/v1/stripe/success?session_id={{CHECKOUT_SESSION_ID}}&user_id={req.user.id}",
            cancel_url=f"{DOMAIN_URL}/api/v1/stripe/cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": price,
                "quantity": 1,
            }]
        )
        return {'success': True, "id": checkout_session["id"],
                'url': checkout_session['url']}

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


class StripeWebhookRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/stripe",
        )

        self.router.add_api_route(
            "/webhook",
            self.webhook_received,
            methods=["POST"],
            description="Stripe Webhook"
        )

    async def webhook_received(self, req: Request,
                               stripe_signature: str = Header(str)):
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
            print(e)
            return {"error": str(e)}

        if event["type"] == "checkout.session.completed":
            session = event_data['object']
            metadata = session.get('metadata')
            if metadata and 'rank' in metadata:
                rank = int(metadata['rank'])
                client_reference_id = session.get(
                    'client_reference_id')  # user id
                user = await self.db.users.get_by_id(int(client_reference_id))
                user.rank = rank
                await self.db.users.update(user)
        elif event["type"] == "invoice.paid":
            print("invoice.paid")
            # print(event_data)

        elif event["type"] == "invoice.payment_failed":
            print("invoice.payment_failed")
            # print(event_data)
        else:
            print("Unhandled event type")
            # print(event_data)

        return {"status": "success"}
