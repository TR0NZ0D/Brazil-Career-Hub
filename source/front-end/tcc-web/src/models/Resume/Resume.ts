import BaseResumeField from "./BaseResumeField";
import Competence from "./Competence";
import Experience from "./Experience";
import Graduation from "./Graduation";
import Link from "./Link";

type Resume = BaseResumeField & {
  title: string;
  description: string;
  competences?: Competence[];
  experiences?: Experience[];
  graduations?: Graduation[];
  links?: Link[];
}

export default Resume;
