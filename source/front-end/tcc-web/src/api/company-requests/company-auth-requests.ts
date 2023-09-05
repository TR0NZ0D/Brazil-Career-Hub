import axios from 'axios';
import { baseUrl } from '../../constants';
import { removeCharsFromCnpj } from 'models/Company/CompanyAccount';

export async function loginCompany(cnpj: string, pass: string, admToken: string) {
  const formData: FormData = new FormData();
  cnpj = removeCharsFromCnpj(cnpj);
  formData.append('cnpj', cnpj);
  formData.append('password', pass);

  return await axios({
    method: "post",
    url: baseUrl + "/api/company/auth/",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
      "Authorization": "Bearer " + admToken
    }
  })
}
