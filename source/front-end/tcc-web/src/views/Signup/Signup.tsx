import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import UserForm from './components/UserForm';
import CompanyForm from './components/CompanyForm';
import UserAccount from 'models/User/UserAccount';

const Signup: FC = () => {

  const [tabValue, setTabValue] = useState(0);
  const [creatingAccount, setCreatingAccount] = useState<boolean>(false);

  function handleCreateUserAccount(
    userName: string,
    name: string,
    surname: string,
    age: number,
    gender: string,
    cpf: string,
    numberOfJobRegistration: number,
    email: string,
    address: string,
    nationality: string,
    languages: string[],
    portfolio: string,
    socialMedia: string,
    contact: string,
    password: string
  ): void {
    setCreatingAccount(true);

    try {
      const user: UserAccount = new UserAccount(userName, password, name, surname, email);

    } catch (error) {
      console.log(error);
    }
  }

  return (
    <Grid container style={{ height: "100%" }}>
      <Grid item xs={2} md={2} sm={0}>
      </Grid>

      <Grid item xs={8} md={8} sm={12}>
        <Container style={{
          borderRadius: "10",
          margin: "7% 0 5% 0",
          border: "2px solid #ebe8e8",
          boxShadow: "0px 4px 4px rgba(0, 0, 0, 0.25)",
          padding: "2%"
        }}>
          <Tabs value={tabValue} onChange={(_, index) => setTabValue(index)} aria-label="options-tab">
            <Tab label="I wanna be hired!" />
            <Tab label="I wanna hire!" />
          </Tabs>

          <Container style={{ padding: "4% 2% 2% 2%" }}>
            <Typography
              variant="h5"
              gutterBottom
              style={{
                marginBottom: "3%",
                fontWeight: "bolder"
              }}
            >
              Sign Up
            </Typography>

            {tabValue === 0 &&
              <UserForm onSubmit={handleCreateUserAccount} />
            }

            {tabValue === 1 &&
              <CompanyForm />
            }
          </Container>
        </Container>
      </Grid>

      <Grid item xs={2} md={2} sm={0}>
      </Grid>
    </Grid>
  )
};

export default Signup;