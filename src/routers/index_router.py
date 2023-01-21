# from __future__ import annotations
#
# import os
#
# from fastapi import APIRouter, Request
# # from fastapi import Depends
# from fastapi.responses import HTMLResponse
# from starlette.responses import RedirectResponse
#
# from src.data import ApplicationDbContext
# from src.utilities import render_template, tokenizer
# from src.models import User
# # from src.dependencies.auth import subscriber_only
#
#
# class IndexRouter:
#     _recaptcha_public_key = os.getenv("RECAPTCHA_PUBLIC")
#
#     def __init__(self, db: ApplicationDbContext):
#         self.db = db
#
#         self.router = APIRouter(prefix="")
#
#         self.router.add_api_route(
#             "/{full_path:path}",
#             self.serve_template,
#             methods=["GET"],
#         )
#
#     async def serve_template(self, req: Request, full_path: str):
#         if full_path in table:
#             return render_template(table[full_path], {"request": req})
#
#         return render_template("404.html", {"request": req})
#
#     async def manage_subscription(self, req: Request):
#         if req.user:
#             return render_template("manage_subscription.html",
#                                    {"request": req})
#         return RedirectResponse("/login")
#
#     async def verify_email(self, token: str):
#         user = await self._verify_token(token, mark_as_verified=True)
#         if user is None:
#             return HTMLResponse("the link is invalid or already used!")
#         return RedirectResponse('/login?m=email-verified')
#
#     async def reset_password(self, req: Request):
#         if req.user:
#             return RedirectResponse("/")
#         return render_template("reset-password-email.html",
#                                {"request": req})
#
#     async def reset_password_verify(self, token: str, req: Request):
#         if req.user:
#             return RedirectResponse("/")
#         user = await self._verify_token(token)
#         if user is None:
#             return HTMLResponse("The link is invalid!")
#         return render_template("reset-password.html",
#                                {"request": req, 'token': token})
#
#     async def _verify_token(self, token: str, mark_as_verified=False) -> User | None:
#         email = tokenizer.decode_token(token)
#         if not email:
#             return
#         user: User = await self.db.users.get_by_email(email)
#         if not user:
#             return
#         if mark_as_verified:
#             user.verified = True
#             await self.db.users.update(user)
#         return user
