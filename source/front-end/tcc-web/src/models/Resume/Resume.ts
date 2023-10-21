import { formatDatePickerDate } from "utilities/DateUtilities";
import BaseResumeField from "./BaseResumeField";
import Competencie from "./Competence";
import Experience from "./Experience";
import Graduation from "./Graduation";
import Link from "./Link";

type Resume = BaseResumeField & {
  id?: number;
  title: string;
  competencies?: Competencie[];
  experiences?: Experience[];
  graduations?: Graduation[];
  links?: Link[];
}

export function fillAllResumePropertiesWithProfilePk(resume: Resume, profilePk: string): void {
  resume.profile_pk = profilePk;

  if (resume.competencies !== undefined && resume.competencies !== null) {
    for (let competence of resume.competencies) {
      competence.profile_pk = profilePk;
    }
  }

  if (resume.experiences !== undefined && resume.experiences !== null) {
    for (let exp of resume.experiences) {
      exp.profile_pk = profilePk;
    }
  }

  if (resume.graduations !== undefined && resume.graduations !== null) {
    for (let gra of resume.graduations) {
      gra.profile_pk = profilePk;
    }
  }

  if (resume.links !== undefined && resume.links !== null) {
    for (let link of resume.links) {
      link.profile_pk = profilePk;
    }
  }
}

export function checkForDefaultValues(resume: Resume): void {
  resume.links = resume.links?.filter(x => {
    if (!x.url || x.url === "") {
      return false;
    }

    if ((!x.title || x.title === "") && (!x.description || x.description === "")) {
      return false;
    }

    return true;
  })
}

export function formatResumeDates(resume: Resume): void {
  if (resume.experiences !== undefined && resume.experiences !== null) {
    for (let exp of resume.experiences) {
      exp.experience_start_time = formatDatePickerDate(exp.experience_start_time!);
      exp.experience_end_time = formatDatePickerDate(exp.experience_end_time!);
    }
  }

  if (resume.graduations !== undefined && resume.graduations !== null) {
    for (let gra of resume.graduations) {
      gra.graduation_start_time = formatDatePickerDate(gra.graduation_start_time!);
      gra.graduation_end_time = formatDatePickerDate(gra.graduation_end_time!);
    }
  }
}

export function formatGetResumesResponseIntoResumeModel(resumesFromResponse: any[]): Resume[] {
  const resumes: Resume[] = [];

  for (const resumeFromResponse of resumesFromResponse) {
    const resume: Resume = {
      id: resumeFromResponse.pk as number,
      title: resumeFromResponse.title as string,
      experiences: resumeFromResponse.all_experiences,
      competencies: resumeFromResponse.all_competencies,
      graduations: resumeFromResponse.all_graduations,
      links: resumeFromResponse.all_links
    }

    resumes.push(resume);
  }

  return resumes;
}

export function formatGetResumeResponseIntoResumeModel(resumeFromResponse: any): Resume {
  return {
    id: resumeFromResponse.pk as number,
    title: resumeFromResponse.title as string,
    experiences: resumeFromResponse.all_experiences,
    competencies: resumeFromResponse.all_competencies,
    graduations: resumeFromResponse.all_graduations,
    links: resumeFromResponse.all_links
  }
}

export default Resume;
