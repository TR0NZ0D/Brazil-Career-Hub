class SocialAccount {
  public twitter: string | undefined;
  public linkedin: string | undefined;
  public facebook: string | undefined;
  public instagram: string | undefined;
  public website: string | undefined;

  constructor(linkedin?: string, twitter?: string, facebook?: string,
    instagram?: string, website?: string) {
    this.linkedin = linkedin;
    this.twitter = twitter;
    this.facebook = facebook;
    this.instagram = instagram;
    this.website = website;
  }
}

export default SocialAccount;