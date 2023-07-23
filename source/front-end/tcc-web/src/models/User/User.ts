abstract class User {
  private _userName: string | undefined;
  public email: string | undefined;
  public name: string | undefined;
  public surname: string | undefined;

  constructor(userName: string, email?: string, name?: string, surname?: string) {
    this.userName = userName;
    this.email = email;
    this.name = name;
    this.surname = surname;
  }

  public get userName(): string | undefined {
    return this._userName;
  }

  public set userName(theUserName: string | undefined) {
    if (theUserName === "" || theUserName === undefined) {
      throw new Error("Invalid userName");
    }

    this._userName = theUserName;
  }
}

export default User;