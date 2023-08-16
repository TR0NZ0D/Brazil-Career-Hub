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
      legal_nature: company.legalNature,
      password: company.password
    },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}

export async function deleteAccount(id: number, admToken: string) {
  return await axios({
    method: 'delete',
    url: baseUrl + "/api/company/",
    params: { pk: id },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
