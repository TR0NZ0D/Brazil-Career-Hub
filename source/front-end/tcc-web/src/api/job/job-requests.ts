import axios, { AxiosResponse } from 'axios';
import { baseUrl } from '../../constants';
import { Job } from 'models/Job/Job';

function createJobAccordingToAddress(job: Job): object {
  if (job.address) {
    return {
      created_by: job.companyId,
      role: job.role,
      description: job.description,
      modality: job.modality,
      salary: job.salary,
      address: {
        address: job.address.address,
        title: job.address.title,
        number: job.address.number
      }
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

export async function getCompanyJobs(companyId: number, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "get",
    url: baseUrl + "/api/vacancy/",
    params: { company_pk: companyId },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}

export async function getJobs(admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "get",
    url: baseUrl + "/api/vacancy/",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
