import {
  Grid,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select
} from '@mui/material';
import useNeverEmptyArray from 'hooks/useNeverEmptyArray';
import Competencie from 'models/Resume/Competence';
import { Fragment } from 'react';

type Props = {
  competencies: Competencie[];
  setCompetences: (competences: Competencie[]) => void;
}

const CompetenceFields = ({ competencies, setCompetences }: Props) => {

  useNeverEmptyArray(competencies, setCompetences);

  function handleCompetenceNameChange(val: string, index: number): void {
    let copy: Competencie[] = [...competencies];
    copy[index].competence_name = val;
    setCompetences(copy);
  }

  function handleCompetenceLevelChange(val: string, index: number): void {
    let copy: Competencie[] = [...competencies];
    copy[index].competence_level = val;
    setCompetences(copy);
  }

  function handleAddCompetence(): void {
    let copy: Competencie[] = [...competencies];
    copy.push({});
    setCompetences(copy);
  }

  function handleDeleteCompetence(): void {
    let copy: Competencie[] = [...competencies];
    copy.pop();
    setCompetences(copy);
  }

  return (
    <>
      <Grid item lg={12}>
        <Typography variant="h6" gutterBottom>Competences</Typography>
      </Grid>

      {competencies.map((x, index) => {
        const competenceId = `competence-label-${index}`;
        return (
          <Fragment key={index}>
            <Grid item lg={12}>
              <Typography variant="body1">Competence {index + 1}</Typography>
            </Grid>

            <Grid item lg={6}>
              <TextField
                id="name"
                label="Name"
                variant="outlined"
                value={x.competence_name}
                onChange={(e) => handleCompetenceNameChange(e.target.value, index)}
                fullWidth
              />
            </Grid>

            <Grid item lg={6}>
              <FormControl fullWidth>
                <InputLabel id={competenceId}>Level</InputLabel>
                <Select
                  labelId={competenceId}
                  id={`competence-select-lbl-${index}`}
                  value={x.competence_level}
                  label="Age"
                  onChange={(e) => handleCompetenceLevelChange(e.target.value, index)}
                >
                  <MenuItem value="1">Beginner</MenuItem>
                  <MenuItem value="2">Amateur</MenuItem>
                  <MenuItem value="3">Intermediate</MenuItem>
                  <MenuItem value="4">Professional</MenuItem>
                  <MenuItem value="5">Master</MenuItem>
                </Select>
              </FormControl>
            </Grid>

          </Fragment>
        )
      })}
      <Grid container item display="flex" justifyContent="flex-end" alignItems="flex-end" lg={12}>
        <Button variant="contained" onClick={handleAddCompetence}>Add competence</Button>

        {competencies.length > 1 &&
          <Button variant="outlined" onClick={handleDeleteCompetence} style={{ marginLeft: "2%" }}>Delete competence</Button>}
      </Grid>
    </>
  )
}

export default CompetenceFields;