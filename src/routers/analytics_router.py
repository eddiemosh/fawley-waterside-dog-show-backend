from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.services.email import EmailService
from src.services.orders import OrderService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


order_service = OrderService()


@router.get("/ticket", status_code=HTTPStatus.OK)
def get_analytics_by_ticket(ticket: str):
    """
    Get analytics for a specific ticket type.
    :param ticket: The name of the ticket type to get analytics for.
    :return: A dictionary containing the analytics data for the specified ticket type.
    """
    try:
        analytics_data = order_service.get_orders_by_ticket(ticket=ticket)
        if not analytics_data:
            raise HTTPException(status_code=404, detail="No analytics data found for this ticket type.")
        return analytics_data
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
