import {
  Button,
  CircularProgress,
  Modal,
  Typography
} from '@mui/material';
import { getUserResumes } from 'api/resume-requests/resume-requests';
import { AuthContext } from 'contexts/AuthContext';
import { UIContext } from 'contexts/UIContext';
import { Job } from 'models/Job/Job';
import Resume, { formatGetResumesResponseIntoResumeModel } from 'models/Resume/Resume';
import UserLogged from 'models/UserLogged/UserLogged';
import { useState, useEffect, useContext } from 'react';
import { DivWrapper, LoadingDiv, MainDiv, ResumeOption, ResumeSelectorBody, ResumeSelectorFooter } from './styles';
import { updateJob } from 'api/job/job-requests';

type Props = {
  show: boolean;
  forJob: Job;
  onClose: () => void;
}

const ResumeSelector = ({ show, forJob, onClose }: Props) => {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResume, setSelectedResume] = useState<number | undefined>();
  const [canApply, setCanApply] = useState<boolean>(false);

  const { loading, setLoading } = useContext(UIContext);
  const { entityLogged, adminToken } = useContext(AuthContext);

  useEffect(() => {
    setLoading(true);
    if (adminToken && entityLogged) {
      const user = entityLogged as UserLogged;
      getUserResumes(user.id, adminToken!)
        .then(response => {
          if (response.status === 200)
            setResumes(formatGetResumesResponseIntoResumeModel(response.data.content));
        })
        .finally(() => setLoading(false));
    }
  }, [adminToken, entityLogged]);

  useEffect(() => {
    if (selectedResume === undefined) {
      setCanApply(false);
      return;
    }

    setCanApply(true);
  }, [selectedResume]);

  function handleApply(): void {
    const resumeId = resumes[selectedResume!].id;
    const jobCopy = { ...forJob };
    jobCopy.resumes!.push(resumeId!);

    updateJob(jobCopy, adminToken!)
      .then(response => {
        if (response.status === 200)
          onClose();
      })
      .catch(() => {
        alert("An error occurred while applying for this job");
      })
  }

  console.log(canApply);
  return (
    <Modal
      open={show}
      onClose={onClose}
    >
      <DivWrapper>
        <MainDiv>
          <Typography variant="h6" gutterBottom>Select your resume for this job:</Typography>

          {loading &&
            <LoadingDiv>
              <CircularProgress />
            </LoadingDiv>}

          {!loading &&
            <>
              <ResumeSelectorBody>
                {resumes.map((x, index) => {
                  const className = index === selectedResume ? "resume-selected" : "";
                  return (
                    <ResumeOption
                      key={x.title}
                      variant="outlined"
                      className={className}
                      onClick={() => setSelectedResume(index)}
                    >
                      {x.title}
                    </ResumeOption>
                  )
                })}
              </ResumeSelectorBody>

              <ResumeSelectorFooter>
                <Button
                  variant="outlined"
                  onClick={onClose}
                >
                  Close
                </Button>

                <Button
                  variant="contained"
                  disabled={!canApply}
                  style={{ marginLeft: "2%" }}
                  onClick={handleApply}
                >
                  Apply
                </Button>
              </ResumeSelectorFooter>
            </>}

        </MainDiv>
      </DivWrapper>
    </Modal>
  )
}

export default ResumeSelector;
