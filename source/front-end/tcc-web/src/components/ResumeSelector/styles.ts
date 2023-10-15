import { Box, Button } from "@mui/material";
import styled from "styled-components";

export const DivWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
`

export const MainDiv = styled.div`
  display: flex;
  background-color: #fff;
  width: 60%;
  height: 70%;
  padding: 2% 3%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
`

export const ResumeSelectorBody = styled.div`
  height: 70%;
  display: flex;
  gap: 10px;
  overflow-y: scroll;
  flex-direction: column;
`

export const LoadingDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
`

export const ResumeOption = styled(Button)`
  &.resume-selected {
    background-color: #3E89FA;
    color: white;
  }
`

export const ResumeSelectorFooter = styled.footer`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 20%;
  width: 100%;
`
