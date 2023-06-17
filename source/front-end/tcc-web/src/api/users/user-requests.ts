import axios from 'axios';
import { UserAccount } from './interfaces/user';
import { baseUrl } from '../../constants';

function appendUserAccountToFormData(fData: FormData, user: UserAccount) {
  if (fData === undefined || fData === null)
    return;

  fData.append("username", user.userName);
  fData.append("password", user.password);
  fData.append("email", user.email);
  fData.append("name", user.name);
  fData.append("surname", user.surname);
}

export function createUserAccount(user: UserAccount) {
  let formBody: FormData = new FormData();
  appendUserAccountToFormData(formBody, user);

  axios({
    method: "post",
    url: baseUrl + "/users",
    data: formBody,
    headers: { "Content-Type": "multipart/formData" }
  })
    .then(response => {

    })
    .catch(response => {
      alert("Could not create your profile!");
    })
}
