import {
  Grid,
  Typography,
  TextField,
  Button
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import useNeverEmptyArray from 'hooks/useNeverEmptyArray';
import Graduation from 'models/Resume/Graduation';
import { Fragment } from 'react';

type Props = {
  graduations: Graduation[];
  setGraduations: (graduations: Graduation[]) => void;
}

const GraduationFields = ({ graduations, setGraduations }: Props) => {

  useNeverEmptyArray(graduations, setGraduations);

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
                id="title"
                label="Title"
                variant="outlined"
                value={x.title}
                onChange={(e) => handleGradiationTitleChange(e.target.value, index)}
                fullWidth
              />
            </Grid>

            <Grid item lg={6}>
              <TextField
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
        <Button variant="contained" onClick={handleAddGraduation}>Add graduation</Button>

        {graduations.length > 1 &&
          <Button variant="outlined" onClick={handleDeleteGraduation} style={{ marginLeft: "2%" }}>Delete graduation</Button>}
      </Grid>
    </>
  )
}

export default GraduationFields;