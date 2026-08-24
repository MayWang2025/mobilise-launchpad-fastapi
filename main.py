from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB_PATH = "/Users/jtwang/Desktop/mobilize_launchpad.db"


@app.get("/worker/{worker_id}/status")
def get_worker_status(worker_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            worker_id,
            name,
            role,
            work_status,
            employment_status,
            work_rights,
            site_induction,
            medical_clearance,
            qualification_status
        FROM Workforce
        WHERE worker_id = ?
        """,
        (worker_id,)
    )

    worker = cursor.fetchone()
    conn.close()

    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    return dict(worker)

class MobilisationRequest(BaseModel):
    worker_id: str
    project: str
    site: str
    start_date: str
    end_date: str
    role: str

@app.post("/mobilisation/request")
def create_mobilisation_request(request: MobilisationRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT worker_id FROM Workforce WHERE worker_id = ?",
        (request.worker_id,)
    )

    worker = cursor.fetchone()

    if worker is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Worker not found")

    cursor.execute("""
        SELECT request_id
        FROM Mobilisation_requests
        ORDER BY request_id DESC
        LIMIT 1
    """)

    last_request = cursor.fetchone()

    if last_request is None:
        request_id = "MOB001"
    else:
        last_number = int(last_request[0].replace("MOB", ""))
        request_id = f"MOB{last_number + 1:03d}"
 

    cursor.execute(
        """
        INSERT INTO Mobilisation_requests
        (
            request_id,
            worker_id,
            project,
            site,
            start_date,
            end_date,
            role,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request_id,
            request.worker_id,
            request.project,
            request.site,
            request.start_date,
            request.end_date,
            request.role,
            "Pending"
        )
    )

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "request_id": request_id,
        "message": "Mobilisation request created",
        "worker_id": request.worker_id
    }