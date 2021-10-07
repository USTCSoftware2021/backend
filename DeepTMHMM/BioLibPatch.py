from biolib.app import BioLibApp
from biolib.biolib_binary_format import ModuleInput
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.app.utils import run_job
from biolib.biolib_api_client import JobState
from biolib.biolib_logging import logger
from biolib.biolib_errors import BioLibError


class BioLibPatch(BioLibApp):
    def __call__(self, sequence_str=None):
        module_input_serialized = self._get_serialized_module_input(sequence_str)

        job = BiolibJobApi.create(self._selected_app_version['public_id'])
        BiolibJobApi.update_state(job['public_id'], JobState.IN_PROGRESS.value)

        try:
            module_output = run_job(job, module_input_serialized)

            try:
                BiolibJobApi.update_state(
                    job_id=job['public_id'], state=JobState.COMPLETED.value)
            except Exception as error:  # pylint: disable=broad-except
                logger.warning(
                    f'Could not update job state to completed:\n{error}')

            return module_output['files']

        except BioLibError as exception:
            logger.error(f'Compute failed with: {exception.message}')
            try:
                BiolibJobApi.update_state(
                    job_id=job['public_id'], state=JobState.FAILED.value)
            except Exception as error:  # pylint: disable=broad-except
                logger.warning(
                    f'Could not update job state to failed:\n{error}')

            raise exception

    @staticmethod
    def _get_serialized_module_input(sequence_str: str) -> bytes:
        files_dict = {"/input.fasta": sequence_str.encode()}
        module_input_serialized: bytes = ModuleInput().serialize(
            stdin="", arguments=["--fasta", "input.fasta"], files=files_dict)
        return module_input_serialized
