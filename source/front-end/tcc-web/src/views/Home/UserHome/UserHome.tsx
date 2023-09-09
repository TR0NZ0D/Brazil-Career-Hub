import { Container, Grid } from '@mui/material';
import { getJobs } from 'api/job/job-requests';
import JobOverview from 'components/JobOverview/JobOverview';
import { AuthContext } from 'contexts/AuthContext';
import useAuthenticated from 'hooks/useAuthenticated';
import { Job } from 'models/Job/Job';
import { useContext, useEffect, useState } from 'react'

const UserHome = () => {
  useAuthenticated("user");

  const { adminToken } = useContext(AuthContext);
  const [vacancies, setVacancies] = useState<Job[]>([]);

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await getJobs(adminToken!);
        setVacancies(response.data.content);
      }
      catch (error) {
        console.error(error);
      }
    }

    getData();
  }, [adminToken]);

  return (
    <Container style={{ margin: "2% 3%" }}>
      <Grid container display="flex">
        <Grid container item lg={9} spacing={3}>
          {vacancies.map((x, index) => {
            return (
              <Grid item lg={12}>
                <JobOverview key={index} job={x} />
              </Grid>
            )
          })}
        </Grid>

        <Grid item lg={3}>

        </Grid>
      </Grid>
    </Container>
  )
}

export default UserHome;
