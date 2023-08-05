type CompanyProfile = {
  id: string | undefined;
  addresses: string[];
  creationDate: Date | undefined;
  financialCapital: number;
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