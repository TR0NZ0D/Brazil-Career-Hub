import styled from "styled-components";

export const Logo = styled.img`
  width: 15%;
  height: 17%;
`;

export const JobCreationContainer = styled.form`
  padding: 3% 4%;
  border-radius: 10px;
  background: #FFF;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
  width: 90%;
  margin-bottom: 5%;
  height: auto;
`;

export const JobApplicantDiv = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 8%;
  width: 90%;
  border: 2px solid #f0f0f0;
  border-radius: 10px;
  padding: 3%;
  margin: 10px 0;
`

export const ResumeViewer = styled.div`
  display: block;
  margin: 15px auto;
  height: 100%;
  width: 45%;
  overflow-y: scroll;

  & > div > div > form {
    height: auto;
  }
`
