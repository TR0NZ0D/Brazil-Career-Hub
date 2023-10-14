import { Grid } from '@mui/material';
import styled from 'styled-components';

export const MainGrid = styled(Grid)`
  padding: 4%;
`;

export const ResumeItem = styled(Grid)`
  padding: 3% 4%;
  border-radius: 10px;
  background: #FFF;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
  height: 4rem;
  margin: 4%;

  &:hover {
    background-color: #F5F5F5;
    transition-duration: 0.5s;
    cursor: pointer;
  }
`
