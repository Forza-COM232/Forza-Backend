# Any endpoints related will be put on this folder.
# This is a sample only!
# Don't put anything on this file, create your own file and make sure to have meaningful name.

from fastapi import APIRouter
from src.forza_backend.services.sample import SampleService
from src.forza_backend.schemas.sample import SampleResponse

router = APIRouter(prefix="/sample")

@router.get("/", response_model=SampleResponse)
def sample_route():
    sample_model = SampleService.get_sample_service()
    return sample_model