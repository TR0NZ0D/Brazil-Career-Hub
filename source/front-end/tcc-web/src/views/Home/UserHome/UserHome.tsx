import { Grid } from '@mui/material';
import { getJobs } from 'api/job/job-requests';
import JobContainerForApply from 'components/JobContainerForApply/JobContainerForApply';
import JobOverview from 'components/JobOverview/JobOverview';
import { AuthContext } from 'contexts/AuthContext';
import useAuthenticated from 'hooks/useAuthenticated';
import { Job } from 'models/Job/Job';
import { useContext, useEffect, useState } from 'react'

const UserHome = () => {
  useAuthenticated("user");

  const { adminToken } = useContext(AuthContext);
  const [vacancies, setVacancies] = useState<Job[]>([]);
  const [jobDetail, setJobDetail] = useState<Job | undefined>();

  function handleJobClick(index: number): void {
    setJobDetail(vacancies[index]);
  }

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
    <Grid container display="flex" style={{ padding: "2% 3%" }}>
      <Grid container item display="flex" justifyContent="space-between">
        <Grid container item lg={5} spacing={1}>
          {vacancies.map((x, index) => {
            return (
              <Grid item lg={12}>
                <JobOverview key={index} job={x} onClick={() => handleJobClick(index)} />
              </Grid>
            )
          })}
        </Grid>

        <Grid item lg={6}>
          {vacancies.length > 0 && jobDetail &&
            <JobContainerForApply job={jobDetail} />}
        </Grid>
      </Grid>
    </Grid>
  )
}

export default UserHome;
