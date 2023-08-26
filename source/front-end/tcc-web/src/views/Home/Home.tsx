import useAuthenticated from 'hooks/useAuthenticated';
import { FC } from 'react';

const Home: FC = () => {
  useAuthenticated();

  return (
    <h2>Home page</h2>
  );
}

export default Home;
