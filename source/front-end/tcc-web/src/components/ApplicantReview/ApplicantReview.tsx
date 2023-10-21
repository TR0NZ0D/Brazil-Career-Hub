import { TextField, Typography } from '@mui/material';
import FieldSeparator from 'components/FieldSeparator/FieldSeparator';
import ResumeForm from 'components/ResumeForm/ResumeForm';
import { JobApplicant } from 'models/JobApplicant/JobApplicant'
import { ContentWrapper } from './styles';

type Props = {
  applicant: JobApplicant;
}

const ApplicantReview = ({ applicant }: Props) => {

  const { profile, resume } = applicant;
  return (
    <ContentWrapper>
      <Typography variant="h6">Contact info</Typography>
      <TextField
        label="email"
        value={profile.email}
        fullWidth
        disabled
      />

      <TextField
        label="Phone"
        value={profile.phone}
        fullWidth
        disabled
      />

      <FieldSeparator />

      <Typography variant="h6">Resume</Typography>
      <ResumeForm
        title={resume.title!}
        experiences={resume.experiences!}
        competencies={resume.competencies!}
        graduations={resume.graduations!}
        links={resume.links!}
        action="read"
      />
    </ContentWrapper>
  )
}

export default ApplicantReview