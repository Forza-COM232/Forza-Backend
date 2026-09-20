# Any business logic will be put in this folder.
# This is just a sample!
# So, don't put anything on this file, create your own file and make sure to have meaningful name.

from uuid import uuid4
from ..core.models.sample import SampleModel

class SampleService():
    
    @staticmethod
    def get_sample_service():
        return SampleModel(
            sample_id=uuid4(),
            name="Sample User"
        )