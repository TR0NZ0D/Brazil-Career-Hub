import axios from 'axios';
import { baseUrl } from '../../constants';
import CompanyAccount from 'models/Company/CompanyAccount';

export async function createAccount(company: CompanyAccount, admToken: string) {
  axios({
    method: 'post',
    url: baseUrl + "/api/company",
    data: company,
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
