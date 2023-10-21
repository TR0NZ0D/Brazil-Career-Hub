import axios, { AxiosResponse } from 'axios';
import { baseUrl } from '../../constants';
import UserProfile from 'models/User/UserProfile';

export function getUserProfile(profileId: number, admToken: string): Promise<AxiosResponse> {
  return axios({
    method: "get",
    url: baseUrl + "/api/users/profile/",
    params: { pk: profileId },
    headers: {
      "Authorization": "Bearer " + admToken,
      "Content-Type": "application/json"
    }
  })
}

export async function createUserProfile(user: UserProfile, admToken: string) {
  return await axios({
    method: "post",
    url: baseUrl + "/api/users/profile/",
    headers: {
      "Authorization": "Bearer " + admToken,
      "Content-Type": "application/json"
    },
    data: user.getJsonForProfileCreation()
  })
}
