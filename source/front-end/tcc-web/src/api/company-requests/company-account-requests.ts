import axios from 'axios';
import { baseUrl } from '../../constants';
import CompanyAccount, { removeCharsFromCnpj } from 'models/Company/CompanyAccount';

export async function createAccount(company: CompanyAccount, admToken: string) {
  return await axios({
    method: 'post',
    url: baseUrl + "/api/company/",
    data: {
      cnpj: removeCharsFromCnpj(company.cnpj!),
      corporate_name: company.corporateName,
      registration_status: company.registrationStatus,
      fantasy_name: company.fantasyName,
      cnae: company.cnae,
      legal_nature: company.legalNature
    },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
