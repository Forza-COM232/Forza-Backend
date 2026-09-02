# Any schema related will be put in this folder.
# This is just a sample!
# So, don't put anything on this file, create your own file and make sure to have meaningful name.

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SampleResponse(BaseModel):
    sample_id: UUID
    name: str
    
    model_config = ConfigDict(from_attributes=True)