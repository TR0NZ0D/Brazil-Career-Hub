import { Dayjs } from "dayjs";

type CompanyProfile = {
  id: string | undefined;
  addresses: string[];
  creationDate: Dayjs | undefined;
  financialCapital: 0 | 1 | 2 | 3;
  employees: number;
  url: string;
  socialMedia: SocialMedia[];
}

type SocialMedia = {
  url: string | undefined;
  title: string | undefined;
  username: string | undefined;
}

export default CompanyProfile;