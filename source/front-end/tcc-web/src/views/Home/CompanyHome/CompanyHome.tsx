import { Button, Container, Grid, Typography } from '@mui/material';
import { useContext, useEffect, useState } from 'react';
import WorkIcon from '@mui/icons-material/Work';
import { HomeContainer } from './styles';
import { useNavigate } from 'react-router-dom';
import useAuthenticated from 'hooks/useAuthenticated';
import { AuthContext } from 'contexts/AuthContext';
import { getCompanyJobs } from 'api/job/job-requests';
import { CompanyAuth } from 'models/Company/CompanyAuth';
import { Job } from 'models/Job/Job';

const CompanyHome = () => {
  useAuthenticated("company");
  const [vacancies, setVacancies] = useState<Job[]>([]);

  const { entityLogged, adminToken } = useContext(AuthContext);

  const navigate = useNavigate();

  useEffect(() => {
    const company = entityLogged as CompanyAuth;
    const fetchJobs = async () => {
      try {
        const result = await getCompanyJobs(company.company_account!, adminToken!);
        setVacancies(result.data.content);
      } catch (error) {
        console.log(error);
      }
    }

    fetchJobs();
  }, [adminToken]);

  return (
    <HomeContainer>

      {vacancies.length > 0 &&
        <div>Hello</div>}

      {vacancies.length === 0 &&
        <>
          <Grid
            container
            display="flex"
            justifyContent="center"
            alignItems="center"
            style={{ height: "30%" }}
          >
            <Grid
              container
              item
              lg={8}
              display="flex"
              flexDirection="column"
              justifyContent="center"
              alignItems="center"
            >
              <WorkIcon sx={{ fontSize: 80 }} style={{ fill: "#3E89FA" }} />
              <Typography variant="h6" gutterBottom>It looks like you haven't created a job</Typography>
              <Button variant="contained" onClick={() => navigate("/createJob")}>Create job</Button>
            </Grid>

            <Grid item lg={4}>
              <Container>
                <Typography gutterBottom>Total of jobs: 1</Typography>
                <Typography gutterBottom>Total of jobs: 1</Typography>
              </Container>
            </Grid>
          </Grid>
        </>}
    </HomeContainer>
  )
}

export default CompanyHome;