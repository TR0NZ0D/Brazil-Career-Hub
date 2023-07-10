import axios from 'axios';
import UserAccount from 'models/User/UserAccount';
import { baseUrl } from '../../constants';

export async function getUserAccount(username: string, admToken: string) {
  return await axios({
    method: "get",
    url: baseUrl + "/api/users?username=" + username,
    headers: { "Authorization": "Bearer " + admToken }
  })
}

export async function createUserAccount(user: UserAccount, admToken: string) {

  return await axios({
    method: "post",
    url: baseUrl + "/api/users/",
    data: {
      "username": user.userName,
      "password": user.password,
      "email": user.email,
      "name": user.name,
      "surname": user.surname
    },
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + admToken
    }
  })
}
