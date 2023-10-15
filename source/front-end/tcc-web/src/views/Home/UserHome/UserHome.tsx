import { CircularProgress, Grid, Typography } from '@mui/material';
import { getJobs } from 'api/job/job-requests';
import JobContainerForApply from 'components/JobContainerForApply/JobContainerForApply';
import JobOverview from 'components/JobOverview/JobOverview';
import { AuthContext } from 'contexts/AuthContext';
import useAuthenticated from 'hooks/useAuthenticated';
import { Job } from 'models/Job/Job';
import { useContext, useEffect, useState } from 'react';
import WorkOffIcon from '@mui/icons-material/WorkOff';
import { UIContext } from 'contexts/UIContext';

const UserHome = () => {
  useAuthenticated("user");

  const { adminToken } = useContext(AuthContext);
  const [vacancies, setVacancies] = useState<Job[]>([]);
  const [jobDetail, setJobDetail] = useState<Job | undefined>();

  const { loading, setLoading } = useContext(UIContext);

  function handleJobClick(index: number): void {
    setJobDetail(vacancies[index]);
  }

  useEffect(() => {
    const getData = async () => {
      try {
        setLoading(true);
        getJobs(adminToken!)
          .then(response => {
            if (response.status === 200) {
              setVacancies(response.data.content);
            }
          })
          .finally(() => setLoading(false));

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
        {vacancies.length > 0 &&
          <Grid container item lg={5} spacing={1}>
            {vacancies.map((x, index) => {
              return (
                <Grid item lg={12}>
                  <JobOverview key={index} job={x} onClick={() => handleJobClick(index)} />
                </Grid>
              )
            })}
          </Grid>}

        {loading &&
          <Grid container item lg={5} display="flex" justifyContent="center" alignItems="center">
            <CircularProgress />
          </Grid>}

        {vacancies.length === 0 && !loading &&
          <Grid
            container
            lg={5}
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
          >
            <WorkOffIcon sx={{ fontSize: 65, color: "#3E89FA" }} />
            <Typography variant="body1">Looks like there is no job posted right now, come back later</Typography>
          </Grid>}

        <Grid item lg={7}>
          {vacancies.length > 0 && jobDetail &&
            <JobContainerForApply job={jobDetail} />}
        </Grid>
      </Grid>
    </Grid>
  )
}

export default UserHome;
