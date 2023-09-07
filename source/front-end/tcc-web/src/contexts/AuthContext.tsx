import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';
import UserProfile from 'models/User/UserProfile';
import { loginUser } from 'api/users-requests/auth-requests';
import { loginCompany } from 'api/company-requests/company-auth-requests';
import { CompanyAuth } from 'models/Company/CompanyAuth';

type ProviderProps = {
  children: ReactNode;
}

type AdminToken = {
  message: string;
  token: string;
}

type AuthContextProps = {
  adminToken: string | undefined;
  entityLogged: CompanyAuth | UserProfile | undefined;
  entityType: "company" | "user" | undefined;

  userLogin: (username: string, pass: string) => Promise<UserProfile | undefined>;
  companyLogin: (cnpj: string, pass: string) => Promise<CompanyAuth | undefined>;
}

export const AuthContext = createContext({} as AuthContextProps);

export const AuthContextProvider = ({ children }: ProviderProps) => {

  const [adminToken, setAdminToken] = useState<string | undefined>();
  const [entityLogged, setEntityLogged] = useState<CompanyAuth | UserProfile>();
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

      if (entity.cnpj !== undefined)
        setEntityType("company");
      else
        setEntityType("user");
    }
  }, [])

  async function userLogin(username: string, pass: string): Promise<UserProfile | undefined> {
    let user: UserProfile | undefined;
    try {
      const response = await loginUser(username, pass, adminToken!);
      if (response.status === 200) {
        user = response.data.content as UserProfile;
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

  return (
    <AuthContext.Provider value={{
      // states
      adminToken,
      entityLogged,
      entityType,

      // methods
      userLogin,
      companyLogin
    }}>
      {children}
    </AuthContext.Provider>
  )
}
