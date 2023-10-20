import {
  Button,
  Container,
  Grid,
  Typography
} from '@mui/material';
import { useContext, useEffect, useState } from 'react';
import WorkIcon from '@mui/icons-material/Work';
import { HomeContainer, JobDetailDiv, JobsDiv } from './styles';
import { useNavigate } from 'react-router-dom';
import useAuthenticated from 'hooks/useAuthenticated';
import { AuthContext } from 'contexts/AuthContext';
import { getCompanyJobs } from 'api/job/job-requests';
import { CompanyAuth } from 'models/Company/CompanyAuth';
import { Job } from 'models/Job/Job';
import JobOverview from 'components/JobOverview/JobOverview';
import JobSearch from 'components/JobSearch/JobSearch';
import JobForm from 'components/JobForm/JobForm';
import { UIContext } from 'contexts/UIContext';

const CompanyHome = () => {

  useAuthenticated("company");
  const [vacanciesOnSearch, setVacanciesOnSearch] = useState<Job[]>([]);
  const [vacancies, setVacancies] = useState<Job[]>([]);
  const [jobSelected, setJobSelected] = useState<Job | undefined>();
  const [showJobForm, setShowJobForm] = useState<boolean>(false);

  const { entityLogged, adminToken } = useContext(AuthContext);
  const { loading, setLoading } = useContext(UIContext);

  const navigate = useNavigate();

  useEffect(() => {
    if (adminToken && entityLogged) {
      getJobs();
    }
  }, [adminToken]);

  function handleJobOverviewClick(index: number): void {
    setJobSelected(vacanciesOnSearch[index]);
    setShowJobForm(true);
  }

  function handleCreateJobClick(): void {
    setJobSelected(undefined);
    setShowJobForm(true);
  }

  function handleJobsUpdate(): void {
    setShowJobForm(false);
    getJobs();
  }

  function getJobs(): void {
    setLoading(true);
    const company = entityLogged as CompanyAuth;
    getCompanyJobs(company.company_account!, adminToken!)
      .then(response => {
        if (response.status === 200) {
          setVacancies(response.data.content);
          setVacanciesOnSearch(response.data.content);
        }
      })
      .finally(() => {
        setLoading(false);
      })
  }

  return (
    <HomeContainer>
      <JobsDiv>

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
                <Button variant="contained" onClick={handleCreateJobClick}>Create job</Button>
              </Grid>
            </Grid>
          </>}

        {vacanciesOnSearch.length > 0 &&
          <>
            <JobSearch allJobs={vacancies} jobs={vacanciesOnSearch} onSearchChange={setVacanciesOnSearch} />
            <Button
              fullWidth
              variant="contained"
              onClick={handleCreateJobClick}
            >
              Create Job
            </Button>

            {vacanciesOnSearch.map((x, index) => {
              return (
                <JobOverview
                  key={index}
                  job={x}
                  onClick={() => handleJobOverviewClick(index)}
                />
              )
            })}
          </>
        }
      </JobsDiv>

      <JobDetailDiv>
        {showJobForm &&
          <JobForm job={jobSelected} onActionExecuted={handleJobsUpdate} />}

      </JobDetailDiv>
    </HomeContainer>
  )
}

export default CompanyHome;