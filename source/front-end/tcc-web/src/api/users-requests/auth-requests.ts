import axios from 'axios';
import { baseUrl } from '../../constants';

export async function loginUser(username: string, pass: string, admToken: string) {
  let formData: FormData = new FormData();
  formData.append('username', username);
  formData.append('password', pass);

  return await axios({
    method: "post",
    url: baseUrl + "/api/users/auth/",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
      "Authorization": "Bearer " + admToken
    }
  })
}
