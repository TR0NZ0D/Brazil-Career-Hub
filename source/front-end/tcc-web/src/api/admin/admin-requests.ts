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

  axios<TokenResponse>({
    method: "post",
    data: formData,
    url: baseUrl + "/auth/token",
    headers: {
      username,
      password,
      "Content-Type": "multipart/form-data",
    }
  })
    .then(resp => {
      console.log(resp);
      if (resp.status === 200) {
        return resp.data;
      }

      return resp;
    })
    .catch(resp => {
      console.log(resp)
      return resp;
    })
}
