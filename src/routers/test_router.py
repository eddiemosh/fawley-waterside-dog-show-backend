from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.services.orders import OrderService

router = APIRouter(prefix="/test", tags=["Test"])


@router.put("/", status_code=HTTPStatus.OK)
def toggle_test_mode(test_mode: bool):
    try:
        order_service = OrderService()
        test_mode = order_service.update_test_mode(test_mode=test_mode)
        return {"message": f"Test mode set to {test_mode}"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/", status_code=HTTPStatus.OK)
def get_test_mode():
    try:
        order_service = OrderService()
        test_mode = order_service.get_test_mode()
        return {"test_mode": test_mode}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
