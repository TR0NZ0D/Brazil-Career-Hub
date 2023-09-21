import BaseResumeField from "./BaseResumeField";

type Experience = BaseResumeField & {
  description?: string;
  experience_company?: string;
  experience_role?: string;
  experience_start_time?: string;
  experience_end_time?: string;
};

export default Experience;
