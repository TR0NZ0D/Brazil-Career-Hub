import { FC, useState, useContext } from 'react';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import UserForm from './components/UserForm';
import CompanyForm from './components/CompanyForm';
import UserAccount from 'models/User/UserAccount';
import { useNavigate } from 'react-router-dom';
import { CircularProgress } from '@mui/material';
import { AuthContext } from 'contexts/AuthContext';
import { createUserAccount, getUserAccount } from 'api/users/user-requests';

const Signup: FC = () => {

  const [tabValue, setTabValue] = useState(0);
  const [creatingAccount, setCreatingAccount] = useState<boolean>(false);

  const { adminToken } = useContext(AuthContext);

  const navigate = useNavigate();

  async function handleCreateUserAccount(
    userName: string,
    name: string,
    surname: string,
    age: number,
    gender: string,
    cpf: string,
    email: string,
    address: string,
    nationality: string,
    languages: string[],
    portfolio: string,
    socialMedia: string,
    contact: string,
    password: string
  ) {
    try {
      setCreatingAccount(true);

      const userAcExists = await userAccountExists(userName!);
      if (!userAcExists) {
        const user: UserAccount = new UserAccount(userName, password, name, surname, email);
        const resp = await createUserAccount(user, adminToken!);
      }

      // navigate("/");
    } catch (error) {
      console.log(error);
    } finally {
      setCreatingAccount(false);
    }
  }

  async function userAccountExists(username: string) {
    try {
      const response = await getUserAccount(username, adminToken!);
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }

  return (
    <Grid container style={{ height: "80%" }}>
      <Grid item xs={2} md={2} sm={0}>
      </Grid>

      {creatingAccount &&
        <Grid
          container
          item
          xs={8}
          md={8}
          sm={8}
          display="flex"
          justifyContent="center"
          alignItems="center"
        >
          <Container
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
              borderRadius: 10,
              backgroundColor: "#f7f6f6",
              width: "40%",
              height: "40%"
            }}
          >
            <CircularProgress />
            <Typography>Creating your account...</Typography>
          </Container>
        </Grid>
      }

      {!creatingAccount &&
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
        </Grid>}

      <Grid item xs={2} md={2} sm={0}>
      </Grid>
    </Grid>
  )
};

export default Signup;