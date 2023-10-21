abstract class User {
  private _userName: string | undefined;
  public email: string | undefined;
  public name: string | undefined;
  public surname: string | undefined;

  constructor(username: string, email?: string, name?: string, surname?: string) {
    this.username = username;
    this.email = email;
    this.name = name;
    this.surname = surname;
  }

  public get username(): string | undefined {
    return this._userName;
  }

  public set username(theUserName: string | undefined) {
    if (theUserName === "" || theUserName === undefined) {
      throw new Error("Invalid userName");
    }

    this._userName = theUserName;
  }
}

export default User;