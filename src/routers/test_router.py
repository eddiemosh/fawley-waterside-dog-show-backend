from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.repositories.test_repository import TestRepository

router = APIRouter(prefix="/test", tags=["Test"])


@router.put("", status_code=HTTPStatus.OK)
def toggle_test_mode():
    try:
        test_repository = TestRepository()
        test_mode = test_repository.toggle_test_mode()
        return {"message": f"Test mode set to {test_mode}"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("", status_code=HTTPStatus.OK)
def get_test_mode():
    try:
        test_repository = TestRepository()
        test_mode = test_repository.get_test_mode()
        return {"test_mode": test_mode}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
