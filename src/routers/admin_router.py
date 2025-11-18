from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("")
def migrate_database():
    try:
        import scratch
        return {"status": "Database migration completed successfully."}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
