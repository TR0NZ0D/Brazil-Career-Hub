import { Button, Typography } from '@mui/material';
import { Job } from 'models/Job/Job';
import { ContentBreaker, JobDetailContainer } from './style';

type Props = {
  job: Job;
}

const JobContainerForApply = ({ job }: Props) => {
  return (
    <JobDetailContainer>
      <Typography variant="h5" gutterBottom>{job.role}</Typography>
      <Typography variant="body2" gutterBottom>{job.company_name}</Typography>
      <Typography variant="body2" gutterBottom>Number of applicants: {job.resumes?.length}</Typography>
      <Button variant="contained">Apply for this job</Button>
      <ContentBreaker />

      <Typography variant="h6" gutterBottom>Description</Typography>
      <Typography variant="body2" gutterBottom>{job.description}</Typography>

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
  )
}

export default JobContainerForApply;