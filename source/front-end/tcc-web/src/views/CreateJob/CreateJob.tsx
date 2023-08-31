import React from 'react';
import { Button, FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField, Typography } from '@mui/material';
import { JobCreationContainer, Logo } from './styles';
import LogoImage from 'assets/images/logo.png';

const CreateJob = () => {
  return (
    <Grid container display="flex" alignItems="center" justifyContent="center" flexDirection="column">
      <Logo src={LogoImage} alt="logo" />

      <JobCreationContainer>
        <Typography variant="h5">Create Job</Typography>

        <Grid container display="flex" spacing={2} style={{ marginTop: "3%" }}>
          <Grid container item display="flex" spacing={2} lg={12} justifyContent="space-around">
            <Grid item lg={6}>
              <TextField
                id="role"
                label="Role"
                variant="outlined"
                fullWidth
              />
            </Grid>

            <Grid item lg={6}>
              <FormControl>
                <FormLabel id="row-modality-group-label">Modality</FormLabel>
                <RadioGroup
                  row
                  aria-labelledby="row-modality-group-label"
                  name="row-modality-buttons-group"
                >
                  <FormControlLabel value="remote" control={<Radio />} label="Remote" />
                  <FormControlLabel value="presencial" control={<Radio />} label="On office" />
                </RadioGroup>
              </FormControl>
            </Grid>
          </Grid>

          <Grid item lg={12}>
            <TextField
              id="description"
              label="Description"
              variant="outlined"
              fullWidth
              multiline
              rows={13}
            />
          </Grid>

          <Grid item lg={6}>
            <TextField
              id="annual-salary"
              label="Annual Salary"
              variant="outlined"
              fullWidth
            />
          </Grid>

          <Grid item lg={6}>
            <TextField
              id="address"
              label="Address"
              variant="outlined"
              fullWidth
            />
          </Grid>
        </Grid>

        <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
          <Button type="submit" variant="contained">Submit</Button>
        </Grid>
      </JobCreationContainer>
    </Grid>
  )
}

export default CreateJob;