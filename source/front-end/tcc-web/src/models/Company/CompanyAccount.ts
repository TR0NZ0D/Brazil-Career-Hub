type CompanyAccount = {
  cnpj: string | undefined;
  registrationStatus: "1" | "2" | "3" | "4" | "5" | "8";
  legalNature: "EI" | "EIRELI" | "SI" | "LTDA" | "SA" | "SLU";
  corporateName: string | undefined;
  fantasyName: string | undefined;
  cnae: string | undefined;
  password: string;
}

export function removeCharsFromCnpj(cnpj: string): string {
  return cnpj.replaceAll('.', '')
    .replace('-', '')
    .replace('/', '');
}

export default CompanyAccount;
