type CompanyAccount = {
  cnpj: string | undefined;
  registrationStatus: "None" | "Active" | "Suspended" | "Inapt" | "Active not regular" | "Extinct";
  legalNature: "Individual Entrepreneur (EI)" | "Individual Limited Liability Company (EIRELI)" | "Simple Society (SI)" | "Private Limited Company (LTDA)" | "Limited Liability Company (SA)" | "Single-Member Limited Company (SLU)";
  corporateName: string | undefined;
  fantasyName: string | undefined;
  cnae: string | undefined;
}

export default CompanyAccount;
