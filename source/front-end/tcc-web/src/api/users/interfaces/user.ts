interface User {
  userName: string;
  email: string;
  name: string;
  surname: string;
}

export interface UserAccount extends User {
  password: string;
}

export interface UserProfile extends User {

}