import { Dayjs } from "dayjs";
import { generateGuid } from "utilities/Generator";

type CompanyProfile = {
  id: number | undefined;
  url: string;
  contact: string;
  creationDate: Dayjs | undefined;
  financialCapital: 0 | 1 | 2 | 3;
  employees: 0 | 1 | 2;
  addresses: CompanyAddress[];
  socialMedia: CompanySocialMedia[];
}

export type CompanyAddress = {
  key?: string;
  title: string;
  address: string;
  number?: number;
}

export type CompanySocialMedia = {
  url: string | undefined;
  title: string | undefined;
  username: string | undefined;
  key?: string;
}

export function addItemToCompanyArray(company: CompanyProfile, type: CompanySocialMedia[] | CompanyAddress[]): CompanyProfile {
  let companyCopy = { ...company };

  if ((type as CompanyAddress[])[0].address !== undefined)
    companyCopy.addresses.push({ address: '', title: '', key: generateGuid() });
  else
    companyCopy.socialMedia.push({ title: '', url: '', username: '', key: generateGuid() });

  return companyCopy;
}

export function removeItemFromCompanyArray(company: CompanyProfile, type: CompanySocialMedia[] | CompanyAddress[]): CompanyProfile {
  let companyCopy = { ...company };

  if ((type as CompanyAddress[])[0].address !== undefined && company.addresses.length > 1)
    companyCopy.addresses.pop();

  else if (company.socialMedia.length > 1)
    companyCopy.socialMedia.pop();

  return companyCopy;
}

export function changeCompanyArrayItem(company: CompanyProfile, type: CompanySocialMedia[] | CompanyAddress[],
  index: number, prop: "address" | "number" | "username" | "url" | "title", val: string): CompanyProfile {
  let companyCopy = { ...company };

  if ((type as CompanyAddress[])[0].address !== undefined && ['address', 'number', 'title'].includes(prop)) {
    switch (prop) {
      case "address":
        companyCopy.addresses[index].address = val;
        break;
      case "title":
        companyCopy.addresses[index].title = val;
        break;
      default:
        companyCopy.addresses[index].number = Number.parseInt(val);
        break;
    }
  }

  else if (['url', 'title', 'username'].includes(prop)) {
    switch (prop) {
      case "url":
        companyCopy.socialMedia[index].url = val;
        break;
      case "title":
        companyCopy.socialMedia[index].title = val;
        break;
      default:
        companyCopy.socialMedia[index].username = val;
        break;
    }
  }

  return companyCopy;
}


export default CompanyProfile;