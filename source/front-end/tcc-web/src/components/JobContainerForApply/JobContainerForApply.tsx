import { Button, Typography } from '@mui/material';
import { Job } from 'models/Job/Job';
import { JobDetailContainer } from './style';
import FieldSeparator from 'components/FieldSeparator/FieldSeparator';
import { useState, useEffect, useContext } from 'react';
import ResumeSelector from 'components/ResumeSelector/ResumeSelector';
import { AuthContext } from 'contexts/AuthContext';
import { UIContext } from 'contexts/UIContext';
import { formatGetResumeRequestIntoResumeModel } from 'models/Resume/Resume';
import { getUserResumes } from 'api/resume-requests/resume-requests';
import UserLogged from 'models/UserLogged/UserLogged';

type Props = {
  job: Job;
}

const JobContainerForApply = ({ job }: Props) => {

  const [showResumeSelector, setShowResumeSelector] = useState<boolean>(false);
  const [userAlreadyApplied, setUserAlreadyApplied] = useState<boolean>(false);

  const { entityLogged, adminToken } = useContext(AuthContext);
  const { setLoading } = useContext(UIContext);

  useEffect(() => {
    setLoading(true);
    if (adminToken && entityLogged) {
      const user = entityLogged as UserLogged;
      getUserResumes(user.id, adminToken!)
        .then(response => {
          if (response.status === 200) {
            const resumes = formatGetResumeRequestIntoResumeModel(response.data.content);
            for (const jobResumes of job?.resumes!) {
              for (const resume of resumes) {
                if (jobResumes === resume.id) {
                  setUserAlreadyApplied(true);
                }
              }
            }
          }
        })
        .finally(() => setLoading(false));
    }
  }, [adminToken, entityLogged]);


  return (
    <>
      <JobDetailContainer>
        <Typography variant="h5" gutterBottom>{job.role}</Typography>
        <Typography variant="body2" gutterBottom>{job.company_name}</Typography>
        <Typography variant="body2" gutterBottom>Number of applicants: {job.resumes?.length}</Typography>

        {!userAlreadyApplied &&
          <Button variant="contained" onClick={() => setShowResumeSelector(true)}>Apply for this job</Button>}

        {userAlreadyApplied &&
          <Typography variant="button">You already applied for this job!</Typography>}

        <FieldSeparator />

        <Typography variant="h6" gutterBottom>Description</Typography>
        <Typography variant="body1" gutterBottom>{job.description}</Typography>

        <Typography variant="h6" gutterBottom>Salary</Typography>
        <Typography variant="body2" gutterBottom>RS{job.salary}</Typography>

        <Typography variant="h6" gutterBottom>Modality</Typography>
        <Typography variant="body2" gutterBottom>{job.modality}</Typography>

        {job.modality === "onsite" &&
          <>
            <Typography variant="h6" gutterBottom>Address</Typography>
            <Typography variant="body2" gutterBottom>{job.address?.address}</Typography>
          </>}
      </JobDetailContainer>

      {showResumeSelector &&
        <ResumeSelector
          forJob={job}
          show={showResumeSelector}
          onClose={() => setShowResumeSelector(false)}
        />}
    </>
  )
}

export default JobContainerForApply;