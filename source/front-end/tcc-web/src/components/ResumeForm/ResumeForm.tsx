import { Grid, Typography, TextField, Button } from '@mui/material';
import FieldSeparator from 'components/FieldSeparator/FieldSeparator';
import Competence from 'models/Resume/Competence';
import Experience from 'models/Resume/Experience';
import Graduation from 'models/Resume/Graduation';
import Link from 'models/Resume/Link';
import CompetenceFields from './CompetenceFields/CompetenceFields';
import ExperienceFields from './ExperienceFields/ExperienceFields';
import GraduationFields from './GraduationFields/GraduationFields';
import LinkFields from './LinkFields/LinkFields';

type Props = {
  title: string;
  experiences: Experience[];
  competences: Competence[];
  graduations: Graduation[];
  links: Link[];

  onTitleChange: (text: string) => void;
  onExperienceChange: (experiences: Experience[]) => void;
  onCompetenceChange: (competences: Competence[]) => void;
  onGraduationsChange: (graduations: Graduation[]) => void;
  onLinksChange: (links: Link[]) => void;
  onSubmit: (event: any) => any;
}

const ResumeForm = ({
  title,
  experiences,
  competences,
  graduations,
  links,

  onTitleChange,
  onExperienceChange,
  onCompetenceChange,
  onGraduationsChange,
  onLinksChange,
  onSubmit

}: Props) => {
  return (
    <form onSubmit={onSubmit}>
      <Grid container item lg={12} spacing={2}>
        <Grid item lg={12}>
          <Typography variant="h6" gutterBottom>Create resume</Typography>
        </Grid>

        <Grid item lg={12}>
          <TextField
            required
            id="title"
            label="Title"
            helperText="Title to help you identify this resume"
            value={title}
            onChange={(e) => onTitleChange(e.target.value)}
            fullWidth
          />
        </Grid>

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <ExperienceFields
          experiences={experiences}
          setExperiences={onExperienceChange} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <CompetenceFields
          competences={competences}
          setCompetences={onCompetenceChange} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <GraduationFields
          graduations={graduations}
          setGraduations={onGraduationsChange} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <LinkFields
          links={links}
          setLinks={onLinksChange} />

        <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
          <Button variant="contained" type="submit">Create resume</Button>
        </Grid>
      </Grid>
    </form>
  )
}

export default ResumeForm;
