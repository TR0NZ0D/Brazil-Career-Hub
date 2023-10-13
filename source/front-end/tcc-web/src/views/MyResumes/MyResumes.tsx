import {
  Button,
  Container,
  Grid,
  Typography
} from "@mui/material";
import Navbar from "components/Navbar/Navbar";
import Resume, {
  fillAllResumePropertiesWithProfilePk,
  formatGetResumeRequestIntoResumeModel,
  formatResumeDates
} from "models/Resume/Resume";
import { useState, useContext, useEffect } from "react";
import ArticleIcon from '@mui/icons-material/Article';
import { MainGrid, ResumeItem } from "./styles";
import Experience from "models/Resume/Experience";
import Competence from "models/Resume/Competence";
import Graduation from "models/Resume/Graduation";
import Link from "models/Resume/Link";
import { AuthContext } from "contexts/AuthContext";
import { createResumeAsync, getUserResumes } from "api/resume-requests/resume-requests";
import UserLogged from "models/UserLogged/UserLogged";
import { setNullIfPropertiesAreEmpty } from "utilities/ObjectUtilites";
import ResumeForm from "components/ResumeForm/ResumeForm";

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

  useEffect(() => {
    if (entityLogged && adminToken) {
      const userLogged = entityLogged as UserLogged;
      const getResumes = async () => {
        const response = await getUserResumes(userLogged.id, adminToken!);
        if (response.status === 200) {
          setResumes(formatGetResumeRequestIntoResumeModel(response.data.content));
        }
      }

      getResumes();
    }

  }, [entityLogged, adminToken]);

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

    setNullIfPropertiesAreEmpty(newResume);
    fillAllResumePropertiesWithProfilePk(newResume, entity.id.toString());
    formatResumeDates(newResume);

    try {
      const response = await createResumeAsync(newResume, adminToken!);

      if (response.status === 201) {
        setSelectedResume(undefined);
        const resumesCopy = [...resumes];
        resumesCopy.push(newResume);
        setResumes(resumesCopy);
      }
    }
    catch (error) {
      console.error(error);
      alert("An error happened while creating this resume!");
    }
  }

  function handleCreateResumeClick(): void {
    setCreating(true);
    setSelectedResume({
      profile_pk: "1",
      title: ""
    });
  }

  function handleResumeClick(index: number): void {
    const resume = resumes[index];
    setSelectedResume(resume);
    setTitle(resume.title);
    setExperiences(resume.experiences!);
    // setCompetences(resume.competences!);
    setGraduations(resume.graduations!);
    setLinks(resume.links!);
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
            <Button variant="contained" onClick={handleCreateResumeClick}>Create resume</Button>
          </Grid>}

        {resumes.length > 0 &&
          <Grid
            container
            item
            display="flex"
            justifyContent="flex-start"
            alignItems="flex-start"
            lg={5}
            spacing={2}>
            {resumes.map((x, index) => (
              <ResumeItem item lg={12} onClick={() => handleResumeClick(index)}>
                <Typography>{x.title}</Typography>
              </ResumeItem>
            ))}

            <Grid container item lg={12} display="flex" justifyContent="flex-start" alignItems="flex-start">
              <Button variant="contained" onClick={handleCreateResumeClick}>Add Resume</Button>
            </Grid>

          </Grid>}

        <Grid container item display="flex" justifyContent="center" lg={7}>
          {selectedResume !== undefined &&
            <Container>
              <ResumeForm
                title={title}
                experiences={experiences}
                competences={competences}
                graduations={graduations}
                links={links}

                onTitleChange={setTitle}
                onExperienceChange={setExperiences}
                onCompetenceChange={setCompetences}
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
