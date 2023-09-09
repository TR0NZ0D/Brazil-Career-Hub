import { AuthContext } from 'contexts/AuthContext';
import { FC, useContext } from 'react';
import CompanyHome from './CompanyHome/CompanyHome';
import useAuthenticated from 'hooks/useAuthenticated';

const Home: FC = () => {
  useAuthenticated("any");
  const { entityType } = useContext(AuthContext);

  return (
    <>
      {entityType === "company" &&
        <CompanyHome />}

      {entityType === "user" &&
        <h2>User home page</h2>}
    </>
  );
}

export default Home;
