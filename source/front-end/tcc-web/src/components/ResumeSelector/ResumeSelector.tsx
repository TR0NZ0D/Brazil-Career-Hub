import { Box, Button, Grid, Modal, Typography } from '@mui/material';
import { getUserResumes } from 'api/resume-requests/resume-requests';
import { AuthContext } from 'contexts/AuthContext';
import { UIContext } from 'contexts/UIContext';
import { Job } from 'models/Job/Job';
import Resume, { formatGetResumeRequestIntoResumeModel } from 'models/Resume/Resume';
import UserLogged from 'models/UserLogged/UserLogged';
import { useState, useEffect, useContext } from 'react';
import { DivWrapper, MainDiv, ResumeOption, ResumeSelectorBody, ResumeSelectorFooter } from './styles';

type Props = {
  show: boolean;
  forJob: Job;
  onClose: () => void;
}

const ResumeSelector = ({ show, forJob, onClose }: Props) => {

  const [resumes, setResumes] = useState<Resume[]>([]);

  const { loading, setLoading } = useContext(UIContext);
  const { entityLogged, adminToken } = useContext(AuthContext);
  const [selectedResume, setSelectedResume] = useState<number | undefined>();

  useEffect(() => {
    setLoading(true);
    if (adminToken && entityLogged) {
      const user = entityLogged as UserLogged;
      getUserResumes(user.id, adminToken!)
        .then(response => {
          if (response.status === 200)
            setResumes(formatGetResumeRequestIntoResumeModel(response.data.content));
        })
        .finally(() => setLoading(false));
    }
  }, [adminToken, entityLogged])

  return (
    <Modal
      open={show}
      onClose={onClose}
    >
      <DivWrapper>
        <MainDiv>
          <Typography variant="h6" gutterBottom>Select your resume for this job:</Typography>
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
              disabled={!selectedResume}
              style={{ marginLeft: "2%" }}
            >
              Apply
            </Button>
          </ResumeSelectorFooter>
        </MainDiv>
      </DivWrapper>
    </Modal>
  )
}

export default ResumeSelector;
