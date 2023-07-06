abstract class User {
  private _userName: string | undefined;
  private _email: string | undefined;
  private _name: string | undefined;
  private _surname: string | undefined;

  constructor(userName: string, email: string, name: string, surname: string) {
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

  public get email(): string | undefined {
    return this._email;
  }

  public set email(theEmail: string | undefined) {
    if (theEmail === "" || theEmail === undefined) {
      throw new Error("Invalid userName");
    }

    this._email = theEmail;
  }

  public get name(): string | undefined {
    return this._name;
  }

  public set name(theName: string | undefined) {
    if (theName === "" || theName === undefined) {
      throw new Error("Invalid userName");
    }

    this._name = theName;
  }

  public get surname(): string | undefined {
    return this._surname;
  }

  public set surname(theSurname: string | undefined) {
    if (theSurname === "" || theSurname === undefined) {
      throw new Error("Invalid userName");
    }

    this._surname = theSurname;
  }
}

export default User;