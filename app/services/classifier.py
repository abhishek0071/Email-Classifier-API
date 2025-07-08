from ..models.email import EmailIn, EmailOut
from .model_registry import registry
from ..core.settings import settings
from .model_loader import options_for

def classify(email: EmailIn, model: str | None = None) -> EmailOut:
    model_name = model or settings.default_model
    label, latency = registry.classify(
            model=model_name,
            subject=email.subject or "",
            body=email.body,
            extra_options=options_for(model_name)  # NEW
        )

    return EmailOut(label=label, model_name=model_name, latency_ms=latency)