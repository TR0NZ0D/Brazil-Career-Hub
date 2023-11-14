import User from "./User";

class UserAccount extends User {
  private _password: string | undefined;

  constructor(userName: string, password: string, name: string, surname: string, email: string) {
    super(userName, email, name, surname);
    this.password = password;
  }

  public get password(): string | undefined {
    return this._password;
  }

  public set password(thePassword: string | undefined) {
    if (thePassword === undefined) {
      throw new Error("Undefined password");
    }

    else if (thePassword.length < 5) {
      throw new Error("Password must contain at least 5 chars")
    }

    this._password = thePassword;
  }
}

export default UserAccount;