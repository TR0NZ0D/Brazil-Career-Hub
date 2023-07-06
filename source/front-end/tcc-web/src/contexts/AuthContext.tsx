import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';

export const AuthContext = createContext({});

type ProviderProps = {
  children: ReactNode;
}

export const AuthContextProvider = ({ children }: ProviderProps) => {

  const [adminToken, setAdminToken] = useState<string | undefined>();

  useEffect(() => {
    function getData() {
      getToken()
        .then(response => console.log(response))
    }

    getData();
  }, []);

  return (
    <AuthContext.Provider value={{
      // states
      adminToken,

      // set states
      setAdminToken
    }}>
      {children}
    </AuthContext.Provider>
  )
}
