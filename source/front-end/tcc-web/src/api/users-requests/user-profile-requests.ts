import axios from 'axios';
import { baseUrl } from '../../constants';
import UserProfile from 'models/User/UserProfile';

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
