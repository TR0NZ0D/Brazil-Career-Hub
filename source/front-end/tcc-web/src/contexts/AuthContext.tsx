import { ReactNode, createContext, useState, useEffect } from 'react';
import { getToken } from 'api/admin/admin-requests';
import CompanyProfile from 'models/Company/CompanyProfile';
import UserProfile from 'models/User/UserProfile';
import { loginUser } from 'api/users-requests/auth-requests';

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

  userLogin: (username: string, pass: string) => Promise<UserProfile | undefined>;
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

  return (
    <AuthContext.Provider value={{
      // states
      adminToken,
      entityLogged,
      userLogin
    }}>
      {children}
    </AuthContext.Provider>
  )
}
