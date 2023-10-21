import { Grid, Typography, TextField, Button } from '@mui/material';
import FieldSeparator from 'components/FieldSeparator/FieldSeparator';
import Competencie from 'models/Resume/Competence';
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
  competencies: Competencie[];
  graduations: Graduation[];
  links: Link[];
  action: "create" | "edit" | "read";

  onTitleChange?: (text: string) => void;
  onExperienceChange?: (experiences: Experience[]) => void;
  onCompetenceChange?: (competencies: Competencie[]) => void;
  onGraduationsChange?: (graduations: Graduation[]) => void;
  onLinksChange?: (links: Link[]) => void;

  onCreate?: (event: any) => any;
  onUpdate?: (event: any) => any;
  onDelete?: (event: any) => any;
}

const ResumeForm = ({
  title,
  experiences,
  competencies,
  graduations,
  links,
  action,

  onTitleChange,
  onExperienceChange,
  onCompetenceChange,
  onGraduationsChange,
  onLinksChange,
  onCreate,
  onUpdate,
  onDelete

}: Props) => {
  return (
    <form>
      <Grid container item lg={12} spacing={2}>
        <Grid item lg={12}>
          {action === "create" && <Typography variant="h6" gutterBottom>Create resume</Typography>}
          {action === "edit" && <Typography variant="h6" gutterBottom>Edit resume</Typography>}

        </Grid>

        <Grid item lg={12}>
          <TextField
            required
            id="title"
            label="Title"
            helperText="Title to help you identify this resume"
            value={title}
            onChange={(e) => onTitleChange && onTitleChange(e.target.value)}
            fullWidth
            disabled={action === "read"}
          />
        </Grid>

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <ExperienceFields
          experiences={experiences}
          setExperiences={onExperienceChange}
          readonly={action === "read"} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <CompetenceFields
          competencies={competencies}
          setCompetences={onCompetenceChange}
          readonly={action === "read"} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <GraduationFields
          graduations={graduations}
          setGraduations={onGraduationsChange}
          readonly={action === "read"} />

        <Grid item lg={12}>
          <FieldSeparator margin={1} />
        </Grid>

        <LinkFields
          links={links}
          setLinks={onLinksChange}
          readonly={action === "read"} />

        {action === "create" &&
          <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
            <Button variant="contained" onClick={onCreate}>Create resume</Button>
          </Grid>}

        {action === "edit" &&
          <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
            <Grid container item lg={2} display="flex" justifyContent="flex-end">
              <Button variant="contained" onClick={onUpdate}>Update</Button>
            </Grid>

            <Grid container item lg={2} display="flex" justifyContent="flex-end">
              <Button variant="outlined" onClick={onDelete}>Delete</Button>
            </Grid>
          </Grid>}

      </Grid>
    </form>
  )
}

export default ResumeForm;
