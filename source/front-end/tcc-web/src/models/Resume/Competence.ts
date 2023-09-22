import BaseResumeField from "./BaseResumeField";

type Competence = BaseResumeField & {
  competence_name?: string;
  competence_level?: string;
}

export default Competence;
