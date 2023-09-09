import {
  Card,
  CardActionArea,
  CardContent,
  Grid,
  Typography
} from '@mui/material';
import { Job } from 'models/Job/Job';
import { cutText } from 'utilities/TextUtilities';

type Props = {
  job: Job;
}

const JobOverview = ({ job }: Props) => {
  let body = job.description;
  body = cutText(body, 250);

  return (
    <Card sx={{ maxWidth: 800 }}>
      <CardActionArea>
        <CardContent>
          <Grid container display="flex" justifyContent="space-between">
            <Typography variant="h6" gutterBottom>{job.role}</Typography>
            <Typography variant="body1" gutterBottom>Applicants: {job.resumes?.length}</Typography>
          </Grid>
          <Typography variant="body2">{body}</Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}

export default JobOverview;
