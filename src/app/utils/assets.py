# AT THIS STAGE, I WILL NOT USE PRESIGNED URLS.

# from fastapi import APIRouter
# from app.utils.s3 import s3_service

# assets_router = APIRouter(prefix="*/assets", tags=["Assets"])

# @assets_router.get("/assets/logo")
# def get_logo_url():
#     return s3_service.generate_presigned_url("rocket.svg")

# @assets_router.get("/assets/oop")
# def get_oop_icon():
#     return s3_service.generate_presigned_url("oopng.png")

# @assets_router.get("/assets/dsa")
# def get_dsa_icon():
#     return s3_service.generate_presigned_url("dsa-icon.svg")
