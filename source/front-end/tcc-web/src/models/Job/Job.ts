import { CompanyAddress } from "models/Company/CompanyProfile";

export type Job = {
  pk?: number;
  role: string;
  description: string;
  modality: "remote" | "onsite";
  salary: number | undefined;
  address?: CompanyAddress | null;
  companyId?: number;
  resumes?: number[];
  created_by?: number;
  company_name?: string;
}