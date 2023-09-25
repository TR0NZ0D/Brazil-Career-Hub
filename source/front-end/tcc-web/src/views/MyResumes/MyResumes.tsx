import {
  Button,
  Container,
  Grid,
  TextField,
  Typography
} from "@mui/material";
import Navbar from "components/Navbar/Navbar";
import Resume, { fillAllResumePropertiesWithProfilePk, formatResumeDates } from "models/Resume/Resume";
import { useState, useContext } from "react";
import ArticleIcon from '@mui/icons-material/Article';
import { MainGrid } from "./styles";
import Experience from "models/Resume/Experience";
import FieldSeparator from "components/FieldSeparator/FieldSeparator";
import ExperienceFields from "./ExperienceFields/ExperienceFields";
import CompetenceFields from "./CompetenceFields/CompetenceFields";
import Competence from "models/Resume/Competence";
import GraduationFields from "./GraduationFields/GraduationFields";
import Graduation from "models/Resume/Graduation";
import LinkFields from "./LinkFields/LinkFields";
import Link from "models/Resume/Link";
import { AuthContext } from "contexts/AuthContext";
import { createResumeAsync } from "api/resume-requests/resume-requests";
import UserLogged from "models/UserLogged/UserLogged";

const MyResumes = () => {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [creating, setCreating] = useState<boolean>(true);
  const [selectedResume, setSelectedResume] = useState<Resume | undefined>();

  const { entityLogged, adminToken } = useContext(AuthContext);

  const [title, setTitle] = useState<string>("");
  const [experiences, setExperiences] = useState<Experience[]>([{}]);
  const [competences, setCompetences] = useState<Competence[]>([{}]);
  const [graduations, setGraduations] = useState<Graduation[]>([{}]);
  const [links, setLinks] = useState<Link[]>([{}]);

  async function handleCreateResume(e: any): Promise<void> {
    e.preventDefault();
    const entity = entityLogged as UserLogged;
    const newResume: Resume = {
      profile_pk: entity.tag,
      title,
      experiences,
      competences,
      graduations,
      links
    };

    fillAllResumePropertiesWithProfilePk(newResume, entity.id.toString());
    formatResumeDates(newResume);

    try {
      const response = await createResumeAsync(newResume, adminToken!);

      if (response.status === 201) {
        setSelectedResume(undefined);
      }
    }
    catch (error) {
      console.error(error);
      alert("An error happened while creating this resume!");
    }
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
            <Button variant="contained" onClick={() => {
              setCreating(true);
              setSelectedResume({ profile_pk: "1", title });
            }}>Create resume</Button>
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

                  <ExperienceFields
                    experiences={experiences}
                    setExperiences={setExperiences} />

                  <Grid item lg={12}>
                    <FieldSeparator margin={1} />
                  </Grid>

                  <CompetenceFields
                    competences={competences}
                    setCompetences={setCompetences} />

                  <GraduationFields
                    graduations={graduations}
                    setGraduations={setGraduations} />

                  <LinkFields
                    links={links}
                    setLinks={setLinks} />

                  <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
                    <Button variant="contained" onClick={handleCreateResume}>Create resume</Button>
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
