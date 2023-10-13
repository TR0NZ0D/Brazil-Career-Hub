import { formatDatePickerDate } from "utilities/DateUtilities";
import BaseResumeField from "./BaseResumeField";
import Competence from "./Competence";
import Experience from "./Experience";
import Graduation from "./Graduation";
import Link from "./Link";

type Resume = BaseResumeField & {
  title: string;
  competences?: Competence[];
  experiences?: Experience[];
  graduations?: Graduation[];
  links?: Link[];
}

export function fillAllResumePropertiesWithProfilePk(resume: Resume, profilePk: string): void {
  resume.profile_pk = profilePk;

  if (resume.competences !== undefined && resume.competences !== null) {
    for (let competence of resume.competences) {
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

export function formatGetResumeRequestIntoResumeModel(resumesFromResponse: any[]): Resume[] {
  const resumes: Resume[] = [];
  for (const resumeFromResponse of resumesFromResponse) {
    const resume: Resume = {
      title: resumeFromResponse.title as string,
      experiences: resumeFromResponse.all_experiences,
      competences: resumeFromResponse.all_competences,
      graduations: resumeFromResponse.all_graduations,
      links: resumeFromResponse.all_links
    }

    resumes.push(resume);
  }

  console.log(resumes);
  return resumes;
}

export default Resume;
