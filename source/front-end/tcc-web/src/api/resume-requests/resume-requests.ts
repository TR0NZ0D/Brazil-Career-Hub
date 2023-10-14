import axios, { AxiosResponse } from 'axios';
import { baseUrl } from '../../constants';
import Resume from 'models/Resume/Resume';

export async function getUserResumes(userId: number, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "get",
    url: baseUrl + "/api/resumes/",
    headers: {
      "Authorization": "Bearer " + admToken
    },
    params: { profile_pk: userId }
  })
}

export async function createResumeAsync(resume: Resume, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "post",
    url: baseUrl + "/api/resumes/",
    data: {
      profile_pk: resume.profile_pk,
      title: resume.title,
      experiences: resume.experiences,
      competencies: resume.competencies,
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

export async function updateResumeAsync(resume: Resume, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "patch",
    url: baseUrl + "/api/resumes/",
    data: {
      profile_pk: resume.profile_pk,
      title: resume.title,
      experiences: resume.experiences,
      competencies: resume.competencies,
      graduations: resume.graduations,
      links: resume.links
    },
    params: { pk: resume.id },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  });
}

export async function deleteResumeAsync(pk: number, admToken: string): Promise<AxiosResponse> {
  return await axios({
    method: "delete",
    url: baseUrl + "/api/resumes/",
    params: { pk },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  });
}
