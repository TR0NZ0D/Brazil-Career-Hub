import BaseResumeField from "./BaseResumeField";

type Link = BaseResumeField & {
  title?: string;
  description?: string;
  url?: string;
}

export default Link;
