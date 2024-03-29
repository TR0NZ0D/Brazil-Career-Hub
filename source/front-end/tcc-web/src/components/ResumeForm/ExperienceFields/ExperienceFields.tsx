import { Grid, Typography, TextField, Button } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import useNeverEmptyArray from 'hooks/useNeverEmptyArray';
import Experience from 'models/Resume/Experience';
import { Fragment } from 'react';

type Props = {
  experiences: Experience[];
  setExperiences?: (experiences: Experience[]) => void;
  readonly?: boolean;
}

const ExperienceFields = ({ experiences, setExperiences, readonly }: Props) => {

  useNeverEmptyArray(experiences, setExperiences);

  function handleExperienceRoleChange(val: string, index: number): void {
    if (setExperiences) {
      let experiencesCopy: Experience[] = [...experiences];
      experiencesCopy[index].experience_role = val;
      setExperiences(experiencesCopy);
    }
  }

  function handleExperienceCompanyChange(val: string, index: number): void {
    if (setExperiences) {
      let experiencesCopy: Experience[] = [...experiences];
      experiencesCopy[index].experience_company = val;
      setExperiences(experiencesCopy);
    }
  }

  function handleExperienceDescriptionChange(val: string, index: number): void {
    if (setExperiences) {
      let experiencesCopy: Experience[] = [...experiences];
      experiencesCopy[index].description = val;
      setExperiences(experiencesCopy);
    }
  }

  function handleExperienceStartDateChange(val: string, index: number): void {
    if (setExperiences) {
      let experiencesCopy: Experience[] = [...experiences];
      experiencesCopy[index].experience_start_time = val;
      setExperiences(experiencesCopy);
    }
  }

  function handleExperienceEndDateChange(val: string, index: number): void {
    if (setExperiences) {
      let experiencesCopy: Experience[] = [...experiences];
      experiencesCopy[index].experience_end_time = val;
      setExperiences(experiencesCopy);
    }
  }

  function handleAddExperience(): void {
    if (setExperiences) {
      let copy: Experience[] = [...experiences];
      copy.push({});
      setExperiences(copy);
    }
  }

  function handleDeleteExperience(): void {
    if (setExperiences) {
      let copy: Experience[] = [...experiences];
      copy.pop();
      setExperiences(copy);
    }
  }

  return (
    <>
      <Grid item lg={12}>
        <Typography variant="h6" gutterBottom>Experiences</Typography>
      </Grid>

      {experiences.map((x, index) => {
        return (
          <Fragment key={index}>
            <Grid item lg={12}>
              <Typography variant="body1">Experience {index + 1}</Typography>
            </Grid>

            <Grid item lg={6}>
              <TextField
                id="role"
                label="Role"
                variant="outlined"
                value={x.experience_role}
                onChange={(e) => handleExperienceRoleChange(e.target.value, index)}
                fullWidth
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={6}>
              <TextField
                id="company"
                label="Company"
                variant="outlined"
                value={x.experience_company}
                onChange={(e) => handleExperienceCompanyChange(e.target.value, index)}
                fullWidth
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={12}>
              <TextField
                id="description"
                label="Description"
                variant="outlined"
                value={x.description}
                onChange={(e) => handleExperienceDescriptionChange(e.target.value, index)}
                fullWidth
                multiline
                rows={10}
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={6}>
              <DatePicker
                label="Start date"
                maxDate={dayjs(new Date())}
                slotProps={{
                  textField: {
                    fullWidth: true
                  }
                }}
                onChange={(e) => handleExperienceStartDateChange(e!.toString(), index)}
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={6}>
              <DatePicker
                label="End date"
                maxDate={dayjs(new Date())}
                slotProps={{
                  textField: {
                    fullWidth: true
                  }
                }}
                onChange={(e) => handleExperienceEndDateChange(e!.toString(), index)}
                disabled={readonly}
              />
            </Grid>

          </Fragment>
        )
      })}

      {!readonly &&
        <>
          <Grid container item display="flex" justifyContent="flex-end" alignItems="flex-end" lg={12}>
            <Button variant="contained" onClick={handleAddExperience}>Add experience</Button>

            {experiences.length > 1 &&
              <Button variant="outlined" onClick={handleDeleteExperience} style={{ marginLeft: "2%" }}>Delete experience</Button>}
          </Grid>
        </>}
    </>
  )
}

export default ExperienceFields;