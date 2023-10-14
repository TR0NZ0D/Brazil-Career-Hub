import {
  Button,
  CircularProgress,
  Container,
  Grid,
  Typography
} from "@mui/material";
import Navbar from "components/Navbar/Navbar";
import Resume, {
  checkForDefaultValues,
  fillAllResumePropertiesWithProfilePk,
  formatGetResumeRequestIntoResumeModel,
  formatResumeDates
} from "models/Resume/Resume";
import { useState, useContext, useEffect } from "react";
import ArticleIcon from '@mui/icons-material/Article';
import { MainGrid, ResumeItem } from "./styles";
import Experience from "models/Resume/Experience";
import Competencie from "models/Resume/Competence";
import Graduation from "models/Resume/Graduation";
import Link from "models/Resume/Link";
import { AuthContext } from "contexts/AuthContext";
import { createResumeAsync, getUserResumes } from "api/resume-requests/resume-requests";
import UserLogged from "models/UserLogged/UserLogged";
import { setNullIfPropertiesAreEmpty } from "utilities/ObjectUtilites";
import ResumeForm from "components/ResumeForm/ResumeForm";
import { UIContext } from "contexts/UIContext";

const MyResumes = () => {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [creating, setCreating] = useState<boolean>(true);
  const [showResumeForm, setShowResumeForm] = useState<boolean>(false);

  const { entityLogged, adminToken } = useContext(AuthContext);
  const { loading, setLoading } = useContext(UIContext);

  const [title, setTitle] = useState<string>("");
  const [experiences, setExperiences] = useState<Experience[]>([{}]);
  const [competencies, setCompetencies] = useState<Competencie[]>([{}]);
  const [graduations, setGraduations] = useState<Graduation[]>([{}]);
  const [links, setLinks] = useState<Link[]>([{}]);

  useEffect(() => {
    setLoading(true);
    if (entityLogged && adminToken) {
      getResumes();
    }

  }, [entityLogged, adminToken]);

  function getResumes(): void {
    if (entityLogged && adminToken) {
      const userLogged = entityLogged as UserLogged;
      setLoading(true);
      getUserResumes(userLogged.id, adminToken!)
        .then(response => {
          if (response.status === 200) {
            setResumes(formatGetResumeRequestIntoResumeModel(response.data.content));
          }
        })
        .finally(() => setLoading(false));
    }
  }

  async function handleCreateResume(e: any): Promise<void> {
    e.preventDefault();
    const entity = entityLogged as UserLogged;
    const newResume: Resume = {
      profile_pk: entity.tag,
      title,
      experiences,
      competencies,
      graduations,
      links
    };

    setNullIfPropertiesAreEmpty(newResume);
    fillAllResumePropertiesWithProfilePk(newResume, entity.id.toString());
    checkForDefaultValues(newResume);
    formatResumeDates(newResume);

    try {
      setLoading(true);
      createResumeAsync(newResume, adminToken!)
        .then(response => {
          if (response.status === 201) {
            setShowResumeForm(false);
            getResumes();
          }
        })
        .finally(() => {
          setLoading(false);
        })

    }
    catch (error) {
      console.error(error);
      alert("An error happened while creating this resume!");
    }
  }

  function handleCreateResumeClick(): void {
    setCreating(true);
    setShowResumeForm(true);
    setTitle("");
    setExperiences([]);
    setCompetencies([]);
    setGraduations([]);
    setLinks([]);
  }

  function handleResumeClick(index: number): void {
    const resume = resumes[index];
    setShowResumeForm(true);
    setTitle(resume.title);
    setExperiences(resume.experiences!);
    setCompetencies(resume.competencies!);
    setGraduations(resume.graduations!);
    setLinks(resume.links!);
  }

  return (
    <>
      <Navbar />
      <MainGrid container display="flex">

        {resumes.length === 0 && !loading && adminToken !== undefined &&
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
            <Button variant="contained" onClick={handleCreateResumeClick}>Create resume</Button>
          </Grid>}

        {loading &&
          <Grid
            container
            item
            display="flex"
            justifyContent="flex-start"
            alignItems="center"
            flexDirection="column"
            lg={5}>
            <CircularProgress />
          </Grid>
        }

        {resumes.length > 0 &&
          <Grid
            container
            item
            display="flex"
            justifyContent="center"
            alignItems="center"
            lg={5}>
            {resumes.map((x, index) => (
              <ResumeItem
                key={x.title}
                item
                lg={12}
                onClick={() => handleResumeClick(index)}>
                <Typography>{x.title}</Typography>
              </ResumeItem>
            ))}

            <Grid container item lg={12} display="flex" justifyContent="flex-start" alignItems="flex-start">
              <Button variant="contained" onClick={handleCreateResumeClick}>Add Resume</Button>
            </Grid>

          </Grid>}

        <Grid container item display="flex" justifyContent="center" lg={7}>
          {showResumeForm &&
            <Container>
              <ResumeForm
                title={title}
                experiences={experiences}
                competencies={competencies}
                graduations={graduations}
                links={links}

                onTitleChange={setTitle}
                onExperienceChange={setExperiences}
                onCompetenceChange={setCompetencies}
                onGraduationsChange={setGraduations}
                onLinksChange={setLinks}
                onSubmit={handleCreateResume}
              />
            </Container>
          }
        </Grid>
      </MainGrid>
    </>
  )
}

export default MyResumes;
