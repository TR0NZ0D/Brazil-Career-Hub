import { Grid, Typography, TextField, Button, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import Competence from 'models/Resume/Competence';
import Experience from 'models/Resume/Experience';
import Graduation from 'models/Resume/Graduation';
import { Fragment } from 'react';

type Props = {
  graduations: Graduation[];
  setGraduations: (graduations: Graduation[]) => void;
}

const CompetenceFields = ({ graduations, setGraduations }: Props) => {

  function handleGradiationTitleChange(val: string, index: number): void {
    let copy: Graduation[] = [...graduations];
    copy[index].title = val;
    setGraduations(copy);
  }

  function handleGraduationTypeChange(val: string, index: number): void {
    let copy: Graduation[] = [...graduations];
    copy[index].graduation_type = val;
    setGraduations(copy);
  }

  function handleGraduationStartChange(val: string, index: number): void {
    let copy: Graduation[] = [...graduations];
    copy[index].graduation_start_time = val;
    setGraduations(copy);
  }

  function handleGraduationEndChange(val: string, index: number): void {
    let copy: Graduation[] = [...graduations];
    copy[index].graduation_end_time = val;
    setGraduations(copy);
  }

  function handleAddGraduation(): void {
    let copy: Graduation[] = [...graduations];
    copy.push({});
    setGraduations(copy);
  }

  function handleDeleteGraduation(): void {
    let copy: Graduation[] = [...graduations];
    copy.pop();
    setGraduations(copy);
  }

  return (
    <>
      <Grid item lg={12}>
        <Typography variant="h6" gutterBottom>Graduations</Typography>
      </Grid>

      {graduations.map((x, index) => {
        return (
          <Fragment key={index}>
            <Grid item lg={12}>
              <Typography variant="body1">Graduation {index + 1}</Typography>
            </Grid>

            <Grid item lg={6}>
              <TextField
                required
                id="title"
                label="title"
                variant="outlined"
                value={x.title}
                onChange={(e) => handleGradiationTitleChange(e.target.value, index)}
                fullWidth
              />
            </Grid>

            <Grid item lg={6}>
              <TextField
                required
                id="type"
                label="Graduation type"
                variant="outlined"
                value={x.graduation_type}
                onChange={(e) => handleGraduationTypeChange(e.target.value, index)}
                fullWidth
              />
            </Grid>

            <Grid item lg={6}>
              <DatePicker
                label="Start date"
                maxDate={dayjs(new Date())}
                slotProps={{
                  textField: {
                    required: true,
                    fullWidth: true
                  }
                }}
                onChange={(e) => handleGraduationStartChange(e!.toString(), index)}
              />
            </Grid>

            <Grid item lg={6}>
              <DatePicker
                label="End date"
                maxDate={dayjs(new Date())}
                slotProps={{
                  textField: {
                    required: true,
                    fullWidth: true
                  }
                }}
                onChange={(e) => handleGraduationEndChange(e!.toString(), index)}
              />
            </Grid>

          </Fragment>
        )
      })}
      <Grid container item display="flex" justifyContent="flex-end" alignItems="flex-end" lg={12}>
        <Button variant="contained" onClick={handleAddGraduation}>Add experience</Button>

        {graduations.length > 1 &&
          <Button variant="outlined" onClick={handleDeleteGraduation} style={{ marginLeft: "2%" }}>Delete experience</Button>}
      </Grid>
    </>
  )
}

export default CompetenceFields;