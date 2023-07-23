import SocialAccount from './SocialAccount';
import User from './User';
import {
  languages as languagesInFile,
  nationalities as nationalitiesInFile
} from 'utilities/RelevantData';
import { Dayjs } from 'dayjs';

class UserProfile extends User {

  private _languages: string[] = [];
  private _nationality: string | undefined;

  public birthDate: Date;
  public gender: "NI" | "M" | "F" | "NB" = "NI";

  constructor(userName: string, public languagesSpoken: string[], gender: "NI" | "M" | "F" | "NB", birthDate: Dayjs,
    nationality: string, public socialAccount: SocialAccount, public biography?: string, public company?: string,
    public cpf?: string, public phone?: string) {
    super(userName);
    this.languages = languagesSpoken;
    this.gender = gender;
    this.birthDate = new Date(birthDate?.year()!, birthDate?.month()!, birthDate?.date());
    this.nationality = nationality;
    this.socialAccount = socialAccount;
    this.biography = biography;
    this.company = company;
    this.cpf = cpf;
    this.phone = phone;
  }

  public get languages(): string[] {
    return this._languages;
  }

  public set languages(langs: string[]) {
    if (langs.length === 0)
      throw new Error("User must speak at least 1 language");

    let langsNotRepeated: string[] = [];
    for (let lang of langs) {
      if (!langsNotRepeated.includes(lang) && languagesInFile.includes(lang)) {
        langsNotRepeated.push(lang);
      }
    }
    this._languages = langsNotRepeated;
  }

  public get nationality(): string {
    return this._nationality!;
  }

  public set nationality(val: string) {
    if (!nationalitiesInFile.includes(val))
      throw new Error("Invalid nationality");

    this._nationality = val;
  }

  public getJsonForProfileCreation() {
    return {
      user_username: this.userName,
      language: "en-us",
      gender: this.gender,
      locale: this.nationality,
      nationality: this.nationality,
      birth_date: this.birthDate !== undefined ? this.birthDate : null,
      biography: this.biography !== undefined ? this.biography : null,
      company: this.company !== undefined ? this.company : null,
      cpf: this.cpf !== undefined ? this.cpf : null,
      phone_number: this.phone !== undefined ? this.phone : null,
      twitter_username: this.socialAccount.twitter !== undefined ? this.socialAccount.twitter : null,
      facebook_username: this.socialAccount.facebook !== undefined ? this.socialAccount.facebook : null,
      linkedin_username: this.socialAccount.linkedin !== undefined ? this.socialAccount.linkedin : null,
      instagram_username: this.socialAccount.instagram !== undefined ? this.socialAccount.instagram : null,
      website: this.socialAccount.website !== undefined ? this.socialAccount.website : null
    }
  }
}

export default UserProfile;
