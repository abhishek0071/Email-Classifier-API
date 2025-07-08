from fastapi import APIRouter, Depends, HTTPException, Query
from ...models.email import EmailIn, EmailOut
from ...services.classifier import classify

router = APIRouter(prefix="/v1", tags=["classifier"])

@router.post("/classify", response_model=EmailOut)
def classify_email(
    email: EmailIn,
    model: str = Query(None, description="Override model, e.g. llama3:8b"),
):
    try:
        return classify(email, model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
