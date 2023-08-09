import { Dayjs } from "dayjs";

type CompanyProfile = {
  id: string | undefined;
  addresses: string[];
  creationDate: Dayjs | undefined;
  financialCapital: 0 | 1 | 2 | 3;
  employees: 0 | 1 | 2;
  url: string;
  socialMedia: CompanySocialMedia[];
}

export type CompanySocialMedia = {
  url: string | undefined;
  title: string | undefined;
  username: string | undefined;
  key: string;
}

export default CompanyProfile;