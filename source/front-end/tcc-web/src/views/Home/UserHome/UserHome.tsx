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
import JobSearch from 'components/JobSearch/JobSearch';
import { JobsDiv, MainDiv } from './styles';

const UserHome = () => {
  useAuthenticated("user");

  const { adminToken } = useContext(AuthContext);
  const [vacanciesOnSearch, setVacanciesOnSearch] = useState<Job[]>([]);
  const [vacancies, setVacancies] = useState<Job[]>([]);
  const [jobDetail, setJobDetail] = useState<Job | undefined>();

  const { loading, setLoading } = useContext(UIContext);

  function handleJobClick(index: number): void {
    setJobDetail(vacancies[index]);
  }

  useEffect(() => {
    setLoading(true);
    const getData = async () => {
      if (adminToken) {
        try {
          getJobs(adminToken!)
            .then(response => {
              if (response.status === 200) {
                setVacancies(response.data.content);
                setVacanciesOnSearch(response.data.content);
              }
            })
            .finally(() => setLoading(false));

        }
        catch (error) {
          console.error(error);
        }
      }
    }

    getData();
  }, [adminToken]);

  return (
    <MainDiv>

      <JobsDiv>
        <JobSearch allJobs={vacancies} jobs={vacanciesOnSearch} onSearchChange={setVacanciesOnSearch} />

        {vacanciesOnSearch.length > 0 &&
          vacanciesOnSearch.map((x, index) => {
            return (
              <JobOverview key={x.pk} job={x} onClick={() => handleJobClick(index)} />
            )
          })
        }

        {loading &&
          <Grid display="flex" justifyContent="center" alignItems="center">
            <CircularProgress />
          </Grid>}

        {vacancies.length === 0 && !loading && adminToken &&
          <Grid
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
          >
            <WorkOffIcon sx={{ fontSize: 65, color: "#3E89FA" }} />
            <Typography variant="body1">Looks like there is no job posted right now, come back later</Typography>
          </Grid>}
      </JobsDiv>

      {vacancies.length > 0 && jobDetail &&
        <JobContainerForApply job={jobDetail} />}
    </MainDiv>
  )
}

export default UserHome;
