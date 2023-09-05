import axios from 'axios';
import { baseUrl } from '../../constants';
import { Job } from 'models/Job/Job';

export async function createJob(job: Job, admToken: string) {
  axios({
    method: "post",
    url: baseUrl + "/api/vacancy/",
    data: job,
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}

