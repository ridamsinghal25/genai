from fastapi import FastAPI, Query, Path
from .queue.connection import queue
from .queue.worker import process_query

app = FastAPI()


@app.post("/")
def simple():
    return {"status": "Server is running"}


@app.post("/chat")
def chat(
    query: str = Query(..., description="The input text to process"),
):
    # Query ko Queue mei daal do
    # User ko bolo your job done
    job = queue.enqueue(process_query, query)
    # internally process_query(query)

    return {"status": "queued", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}
