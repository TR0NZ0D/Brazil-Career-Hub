import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';

type ProviderProps = {
  children: ReactNode;
}

type AdminToken = {
  message: string;
  token: string;
}

type AuthContextProps = {
  adminToken: string | undefined;
}

export const AuthContext = createContext({} as AuthContextProps);

export const AuthContextProvider = ({ children }: ProviderProps) => {

  const [adminToken, setAdminToken] = useState<string | undefined>();

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
      adminToken
    }}>
      {children}
    </AuthContext.Provider>
  )
}
