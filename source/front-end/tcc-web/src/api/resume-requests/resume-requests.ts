import axios, { AxiosResponse } from 'axios';
import { baseUrl } from '../../constants';
import Resume from 'models/Resume/Resume';

export async function createResumeAsync(resume: Resume, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "post",
    url: baseUrl + "/api/resumes/",
    data: {
      profile_pk: resume.profile_pk,
      title: resume.title,
      experiences: resume.experiences,
      competences: resume.competences,
      graduations: resume.graduations,
      links: resume.links,
      projects: null,
      references: null,
      courses: null
    },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  });
}
