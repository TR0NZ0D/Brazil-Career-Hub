import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';
import { loginUser } from 'api/users-requests/auth-requests';
import { loginCompany } from 'api/company-requests/company-auth-requests';
import { CompanyAuth } from 'models/Company/CompanyAuth';
import UserLogged from 'models/UserLogged/UserLogged';

type ProviderProps = {
  children: ReactNode;
}

type AdminToken = {
  message: string;
  token: string;
}

type AuthContextProps = {
  adminToken: string | undefined;
  entityLogged: CompanyAuth | UserLogged | undefined;
  entityType: "company" | "user" | undefined;

  userLogin: (username: string, pass: string) => Promise<UserLogged | undefined>;
  companyLogin: (cnpj: string, pass: string) => Promise<CompanyAuth | undefined>;
  logout: () => void;
}

export const AuthContext = createContext({} as AuthContextProps);

export const AuthContextProvider = ({ children }: ProviderProps) => {

  const [adminToken, setAdminToken] = useState<string | undefined>();
  const [entityLogged, setEntityLogged] = useState<CompanyAuth | UserLogged>();
  const [entityType, setEntityType] = useState<"company" | "user" | undefined>();

  useEffect(() => {
    function getData() {
      getToken()
        .then(response => {
          const data: AdminToken = response.data;
          setAdminToken(data.token);
        })
    }

    getData();
  }, []);

  useEffect(() => {
    const entityOnStorage = localStorage.getItem("entity-logged");
    if (entityOnStorage !== null) {
      const entity = JSON.parse(entityOnStorage);
      setEntityLogged(entity);
    }
  }, [])

  useEffect(() => {
    if (entityLogged !== undefined) {
      const entity = JSON.parse(JSON.stringify(entityLogged));

      if (entity.cnpj !== undefined)
        setEntityType("company");
      else
        setEntityType("user");
    }

  }, [entityLogged])

  async function userLogin(username: string, pass: string): Promise<UserLogged | undefined> {
    let user: UserLogged | undefined;
    try {
      const response = await loginUser(username, pass, adminToken!);
      if (response.status === 200) {
        user = response.data.content as UserLogged;
      }
    } catch (error) {
      console.log(error);
    }

    setEntityLogged(user);
    localStorage.setItem("entity-logged", JSON.stringify(user));
    return user;
  }

  async function companyLogin(cnpj: string, pass: string): Promise<CompanyAuth | undefined> {
    let company: CompanyAuth | undefined;
    try {
      const response = await loginCompany(cnpj, pass, adminToken!);
      if (response.status === 200) {
        company = response.data.content as CompanyAuth;
      }
    } catch (error) {
      console.log(error);
    }

    setEntityLogged(company);
    localStorage.setItem("entity-logged", JSON.stringify(company));
    return company;
  }

  function logout(): void {
    localStorage.removeItem("entity-logged");
  }

  return (
    <AuthContext.Provider value={{
      // states
      adminToken,
      entityLogged,
      entityType,

      // methods
      userLogin,
      companyLogin,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}
