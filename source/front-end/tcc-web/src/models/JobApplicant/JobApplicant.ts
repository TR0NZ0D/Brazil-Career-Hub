import Resume from "models/Resume/Resume";
import UserProfile from "models/User/UserProfile";

export type JobApplicant = {
  profile: UserProfile;
  resume: Resume;
}
