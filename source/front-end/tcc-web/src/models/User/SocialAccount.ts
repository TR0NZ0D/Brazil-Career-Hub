class SocialAccount {
  constructor(public linkedin?: string, public twitter?: string, public facebook?: string,
    public instagram?: string, public website?: string) {
    this.linkedin = linkedin;
    this.twitter = twitter;
    this.facebook = facebook;
    this.instagram = instagram;
    this.website = website;
  }
}

export default SocialAccount;