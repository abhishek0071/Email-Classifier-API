from fastapi import APIRouter, HTTPException, Query
from ...models.email import EmailIn, EmailOut
from ...services.classifier import classify
from ...services.model_loader import detect_format

router = APIRouter(prefix="/v2", tags=["classifier v2"])

@router.post("/classify", response_model=EmailOut)
def classify_email_v2(
    email: EmailIn,
    model: str = Query("gemma3:1b", description="Model or path, e.g. spam.gguf-v2"),
):
    # extra validation: v2 only accepts models in allowed list OR *.gguf-v2 files
    if not model.endswith(".gguf-v2") and detect_format(model) == "other":
        raise HTTPException(400, "v2 requires a gguf-v2 file or valid model id")
    return classify(email, model)
