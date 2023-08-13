import axios from 'axios';
import { baseUrl } from '../../constants';
import CompanyProfile from 'models/Company/CompanyProfile';

export async function createCompanyProfile(profile: CompanyProfile, admToken: string) {
  return await axios({
    method: 'post',
    url: baseUrl + "/api/company/profile/",
    data: {
      company_id: profile.id,
      address: profile.addresses,
      contact: profile.contact,
      financial_capital: profile.financialCapital,
      employees: profile.employees,
      site_url: profile.url,
      social_media: profile.socialMedia
    },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}