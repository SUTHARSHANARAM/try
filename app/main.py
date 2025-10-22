from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from .model import load_model, predict_proba
import time

app = FastAPI(title="AI Demo - Iris Classifier")

# Metrics
REQUEST_COUNT = Counter("requests_total", "Total HTTP requests", ["path", "method", "status"])
INFER_LATENCY = Histogram("inference_seconds", "Time spent in inference")

class PredictRequest(BaseModel):
    features: conlist(float, min_length=4, max_length=4)

class PredictResponse(BaseModel):
    label: int
    probabilities: conlist(float, min_length=3, max_length=3)

model = load_model()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    start = time.time()
    try:
        label, proba = predict_proba(model, req.features)
        status = 200
        return {"label": int(label), "probabilities": [float(x) for x in proba]}
    except Exception as e:
        status = 400
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        INFER_LATENCY.observe(time.time() - start)
        REQUEST_COUNT.labels(path="/predict", method="POST", status=str(status)).inc()
