import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import UserForm from './components/UserForm';
import CompanyForm from './components/CompanyForm';

const Signup: FC = () => {

  const [tabValue, setTabValue] = useState(0);

  return (
    <Grid container style={{ height: "80%" }}>
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
              <UserForm />
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