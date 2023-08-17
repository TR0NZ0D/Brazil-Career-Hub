import { Container, Grid, Typography } from "@mui/material";
import styled from "styled-components";

export const Logo = styled.img`
  width: 15%;
  height: 20%;
`

export const LoginTitle = styled(Typography)`
  font-weight: bold;
`

export const LoginContainer = styled(Grid)`
  padding: 4% 4%;
  border-radius: 10px;
  background: #FFF;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
  height: 100%;
  width: 65% !important;
`