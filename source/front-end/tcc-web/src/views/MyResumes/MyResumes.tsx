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
  formatGetResumesResponseIntoResumeModel,
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
import {
  createResumeAsync,
  deleteResumeAsync,
  getUserResumes,
  updateResumeAsync
} from "api/resume-requests/resume-requests";
import UserLogged from "models/UserLogged/UserLogged";
import { setNullIfPropertiesAreEmpty } from "utilities/ObjectUtilites";
import ResumeForm from "components/ResumeForm/ResumeForm";
import { UIContext } from "contexts/UIContext";
import useAuthenticated from "hooks/useAuthenticated";

const MyResumes = () => {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [showResumeForm, setShowResumeForm] = useState<boolean>(false);

  const { entityLogged, adminToken } = useContext(AuthContext);
  const { loading, setLoading } = useContext(UIContext);

  const [id, setId] = useState<number | undefined>();
  const [title, setTitle] = useState<string>("");
  const [experiences, setExperiences] = useState<Experience[]>([{}]);
  const [competencies, setCompetencies] = useState<Competencie[]>([{}]);
  const [graduations, setGraduations] = useState<Graduation[]>([{}]);
  const [links, setLinks] = useState<Link[]>([{}]);

  useAuthenticated("user");

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
            setResumes(formatGetResumesResponseIntoResumeModel(response.data.content));
          }
        })
        .finally(() => setLoading(false));
    }
  }

  async function handleCreateResume(): Promise<void> {
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
    setId(undefined);
    setShowResumeForm(true);
    setTitle("");
    setExperiences([]);
    setCompetencies([]);
    setGraduations([]);
    setLinks([]);
  }

  function handleResumeClick(index: number): void {
    const resume = resumes[index];
    setId(resume.id!);
    setShowResumeForm(true);
    setTitle(resume.title);
    setExperiences(resume.experiences!);
    setCompetencies(resume.competencies!);
    setGraduations(resume.graduations!);
    setLinks(resume.links!);
  }

  function handleUpdateResume(): void {
    const entity = entityLogged as UserLogged;
    const newResume: Resume = {
      id,
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

    setLoading(true);
    updateResumeAsync(newResume, adminToken!)
      .then(response => {
        if (response.status === 200) {
          setShowResumeForm(false);
          getResumes();
        }
      })
      .finally(() => setLoading(false));
  }

  function handleDeleteResume(): void {
    setLoading(true);
    deleteResumeAsync(id!, adminToken!)
      .then(response => {
        if (response.status === 204) {
          setShowResumeForm(false);
          getResumes();
        }
      })
      .finally(() => setLoading(false))
  }

  return (
    <>
      <Navbar />
      <MainGrid container display="flex">

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

        {resumes.length === 0 && !loading && adminToken !== undefined &&
          <Grid
            container
            item
            display="flex"
            justifyContent="flex-start"
            alignItems="center"
            flexDirection="column"
            lg={5}
          >
            <ArticleIcon sx={{ fontSize: 110, color: "#3E89FA" }} />
            <Typography gutterBottom>Looks like you didn't create a resume yet</Typography>
            <Button variant="contained" onClick={handleCreateResumeClick}>Create resume</Button>
          </Grid>}

        {resumes.length > 0 &&
          <>
            <Grid item lg={12}>
              <Typography variant="h5" gutterBottom>My Resumes</Typography>
            </Grid>

            <Grid
              container
              item
              display="flex"
              justifyContent="flex-start"
              alignItems="flex-start"
              lg={5}
              height="17rem"
            >
              <Grid container item lg={12}
                style={{
                  maxHeight: "24rem",
                  overflowY: "scroll",
                  marginBottom: "4%",
                }}>
                {resumes.map((x, index) => (
                  <ResumeItem
                    key={x.title}
                    onClick={() => handleResumeClick(index)}>
                    <Typography>{x.title}</Typography>
                  </ResumeItem>
                ))}
              </Grid>
              <Button variant="contained" onClick={handleCreateResumeClick}>Add Resume</Button>
            </Grid>
          </>}

        <Grid container item display="flex" justifyContent="center" lg={7}>
          {showResumeForm &&
            <Container>
              <ResumeForm
                title={title}
                experiences={experiences}
                competencies={competencies}
                graduations={graduations}
                links={links}
                action={id === undefined ? "create" : "edit"}

                onTitleChange={setTitle}
                onExperienceChange={setExperiences}
                onCompetenceChange={setCompetencies}
                onGraduationsChange={setGraduations}
                onLinksChange={setLinks}
                onCreate={handleCreateResume}
                onUpdate={handleUpdateResume}
                onDelete={handleDeleteResume}
              />
            </Container>
          }
        </Grid>
      </MainGrid >
    </>
  )
}

export default MyResumes;
