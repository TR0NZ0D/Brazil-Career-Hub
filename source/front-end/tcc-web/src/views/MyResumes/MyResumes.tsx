import { Button, Container, Grid, TextField, Typography } from "@mui/material";
import Navbar from "components/Navbar/Navbar";
import Resume from "models/Resume/Resume";
import { useState } from "react";
import ArticleIcon from '@mui/icons-material/Article';
import { MainGrid } from "./styles";
import Experience from "models/Resume/Experience";
import FieldSeparator from "components/FieldSeparator/FieldSeparator";
import { DatePicker } from "@mui/x-date-pickers";
import dayjs, { Dayjs } from 'dayjs';

const MyResumes = () => {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [creating, setCreating] = useState<boolean>(true);

  const [title, setTitle] = useState<string>("");
  const [experiences, setExperiences] = useState<Experience[]>([]);

  function handleCreateResume(): void {

  }

  return (
    <>
      <Navbar />
      <MainGrid container>

        {resumes.length === 0 &&
          <Grid
            container
            item
            display="flex"
            justifyContent="flex-start"
            alignItems="center"
            flexDirection="column"
            lg={5}>
            <ArticleIcon sx={{ fontSize: 110, color: "#3E89FA" }} />
            <Typography gutterBottom>Looks like you didn't create a resume yet</Typography>
            <Button variant="contained" onClick={() => setCreating(true)}>Create resume</Button>
          </Grid>}

        <Grid container item display="flex" justifyContent="center" lg={7}>
          {creating &&
            <Container>
              <form onSubmit={handleCreateResume}>
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
                      onChange={(e) => setTitle(e.target.value)}
                      fullWidth
                    />
                  </Grid>

                  <Grid item lg={12}>
                    <FieldSeparator margin={1} />
                  </Grid>

                  <Grid item lg={12}>
                    <Typography variant="h6" gutterBottom>Experiences</Typography>
                  </Grid>

                  <Grid item lg={6}>
                    <TextField
                      required
                      id="role"
                      label="Role"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      fullWidth
                    />
                  </Grid>

                  <Grid item lg={6}>
                    <TextField
                      required
                      id="company"
                      label="Company"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      fullWidth
                    />
                  </Grid>

                  <Grid item lg={12}>
                    <TextField
                      required
                      id="description"
                      label="Description"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      fullWidth
                      multiline
                      rows={10}
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
                    />
                  </Grid>

                  <Grid container item display="flex" justifyContent="flex-end" lg={12}>
                    <Button variant="contained">Add experience</Button>
                  </Grid>
                </Grid>
              </form>
            </Container>
          }
        </Grid>
      </MainGrid>
    </>
  )
}

export default MyResumes;
