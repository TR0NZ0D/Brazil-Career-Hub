import {
  Card,
  CardActionArea,
  CardContent,
  Grid,
  Typography
} from '@mui/material';
import { Job } from 'models/Job/Job';
import { cutText } from 'utilities/TextUtilities';
import { JobOverviewCard, JobOverviewCardHeader } from './styles';

type Props = {
  job: Job;
  onClick?: (job: Job) => any;
}

const JobOverview = ({ job, onClick }: Props) => {

  function handleCardClick() {
    if (onClick) {
      onClick(job);
    }
  }

  let body = job.description;
  body = cutText(body!, 250);

  return (
    <JobOverviewCard onClick={handleCardClick}>
      <JobOverviewCardHeader>
        <Typography variant="h6" gutterBottom>{job.role}</Typography>
        <Typography variant="body1" gutterBottom>Applicants: {job.resumes?.length}</Typography>
      </JobOverviewCardHeader>
      <Typography variant="body2">{body}</Typography>
    </JobOverviewCard>
  )
}

export default JobOverview;
