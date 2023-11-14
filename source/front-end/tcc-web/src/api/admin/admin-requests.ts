import axios from 'axios';
import { baseUrl } from '../../constants';

type TokenResponse = {
  status: string,
  message: string,
  token: string
}

export async function getToken() {
  let formData: FormData = new FormData();
  const username: string = "gustavo";
  const password: string = "Aa.123456";

  formData.append("username", username);
  formData.append("password", password);

  return await axios<TokenResponse>({
    method: "post",
    data: formData,
    url: baseUrl + "/api/auth/token/",
    headers: {
      username: username,
      password: password,
      "Content-Type": "multipart/form-data",
    }
  })
}
