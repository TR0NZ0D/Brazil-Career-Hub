import { CompanyAddress } from "models/Company/CompanyProfile";

export type Job = {
  role: string;
  description: string;
  modality: "remote" | "onsite";
  salary: number | undefined;
  address?: CompanyAddress | null;
  companyId?: number;
}