import BaseResumeField from "./BaseResumeField";

type Competencie = BaseResumeField & {
  competence_name?: string;
  competence_level?: string;
}

export default Competencie;
