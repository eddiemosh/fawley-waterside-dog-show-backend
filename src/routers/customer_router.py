# from datetime import datetime, timezone
# from http import HTTPStatus
# from typing import Optional
#
# from fastapi import APIRouter, HTTPException
#
# from src.services.email_service import EmailService
# from src.services.order_service import OrderService
#
# router = APIRouter(prefix="/customer", tags=["Customers"])
#
# customer_service = CustomerService()
#
#
# @router.get("")
# def get_customer(customer_id: Optional[str] = None):
#     try:
#         if customer_id:
#             customer = order_service.get_customer(customer_id=customer_id)
#             if customer:
#                 return customer
#             raise HTTPException(status_code=404, detail="Customer Not Found")
#         else:
#             customers = order_service.get_customers()
#             return customers
#     except Exception as ex:
#         raise HTTPException(status_code=500, detail=str(ex))
