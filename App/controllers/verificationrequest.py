from App.models import VerificationRequest
from App.database import db

def delete_request(request_id):
    request = VerificationRequest.query.get(request_id)
    if not request:
        raise ValueError(f"No verification request found with ID {request_id}")
    db.session.delete(request)
    db.session.commit()