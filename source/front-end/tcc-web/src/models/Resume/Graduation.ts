import BaseResumeField from "./BaseResumeField";

type Graduation = BaseResumeField & {
  title: string;
  graduation_type: string;
  graduation_start_time: string;
  graduation_end_time: string;
}

export default Graduation;