import axios from 'axios';
import { baseUrl } from '../../constants';
import { Job } from 'models/Job/Job';

function createJobAccordingToAddress(job: Job): object {
  if (job.address) {
    return {
      created_by: job.companyId,
      role: job.role,
      description: job.description,
      modality: job.modality,
      salary: job.salary
    }
  }

  return {
    created_by: job.companyId,
    role: job.role,
    description: job.description,
    modality: job.modality,
    salary: job.salary,
    address: job.address
  }
}

export async function createJob(job: Job, admToken: string) {
  const data = createJobAccordingToAddress(job);
  await axios({
    method: "post",
    url: baseUrl + "/api/vacancy/",
    data: data,
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
