import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';
import CompanyProfile from 'models/Company/CompanyProfile';
import UserProfile from 'models/User/UserProfile';

type ProviderProps = {
  children: ReactNode;
}

type AdminToken = {
  message: string;
  token: string;
}

type AuthContextProps = {
  adminToken: string | undefined;
  entityLogged: CompanyProfile | UserProfile | undefined;
}

export const AuthContext = createContext({} as AuthContextProps);

export const AuthContextProvider = ({ children }: ProviderProps) => {

  const [adminToken, setAdminToken] = useState<string | undefined>();
  const [entityLogged, setEntityLogged] = useState<CompanyProfile | UserProfile>();

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

  return (
    <AuthContext.Provider value={{
      // states
      adminToken,
      entityLogged
    }}>
      {children}
    </AuthContext.Provider>
  )
}
