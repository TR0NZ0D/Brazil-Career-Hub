import {
  Button,
  Container,
  Grid,
  Typography
} from '@mui/material';
import { useContext, useEffect, useState } from 'react';
import WorkIcon from '@mui/icons-material/Work';
import { HomeContainer } from './styles';
import { useNavigate } from 'react-router-dom';
import useAuthenticated from 'hooks/useAuthenticated';
import { AuthContext } from 'contexts/AuthContext';
import { getCompanyJobs } from 'api/job/job-requests';
import { CompanyAuth } from 'models/Company/CompanyAuth';
import { Job } from 'models/Job/Job';
import JobOverview from 'components/JobOverview/JobOverview';

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

        if (result.status === 200) {
          setVacancies(result.data.content);
        }
      } catch (error) {
        console.log(error);
      }
    }

    fetchJobs();
  }, [adminToken]);

  function getTotalApplicants(): number {
    let total = 0;
    for (const item of vacancies) {
      total += item.resumes!.length;
    }

    return total;
  }

  return (
    <HomeContainer>
      {vacancies.length > 0 &&
        <>
          <Grid
            container
            display="flex"
            justifyContent="space-around"
            spacing={3}
          >
            <Grid
              container
              item
              lg={9}
              display="flex"
              flexDirection="row"
              spacing={2}
            >
              {vacancies.map((x, index) => {
                return (
                  <Grid item lg={12}>
                    <JobOverview job={x} key={index} />
                  </Grid>
                )
              })}
            </Grid>

            <Grid item lg={3}>
              <Container style={{ padding: "5%" }}>
                <Typography>Total jobs: {vacancies.length}</Typography>
                <Typography gutterBottom>Total applicants: {getTotalApplicants()}</Typography>
                <Button variant="contained" onClick={() => navigate("/createJob")}>Create Job</Button>
              </Container>
            </Grid>
          </Grid>
        </>}

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
              {/* Add job detail */}
            </Grid>
          </Grid>
        </>}
    </HomeContainer>
  )
}

export default CompanyHome;