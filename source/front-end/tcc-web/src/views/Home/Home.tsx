import { AuthContext } from 'contexts/AuthContext';
import { FC, useContext } from 'react';
import CompanyHome from './CompanyHome/CompanyHome';
import useAuthenticated from 'hooks/useAuthenticated';
import UserHome from './UserHome/UserHome';

const Home: FC = () => {
  useAuthenticated("any");
  const { entityType } = useContext(AuthContext);

  return (
    <>
      {entityType === "company" &&
        <CompanyHome />}

      {entityType === "user" &&
        <UserHome />}
    </>
  );
}

export default Home;
