import styled from 'styled-components';
import { Typography, Grid } from '@mui/material';

export const Nav = styled(Grid)`
  background-color: ${props => props.theme.colors.primary};
  padding: 0 2%;
  height: 8%;
`

export const MenuDiv = styled(Grid)`
  padding: 0 1%;
`

export const OptionGrid = styled(Grid)`
  &.active {
    border-bottom: 2px solid white;
  }
`

export const LinkMenu = styled(Typography)`
  color: #fff;
  font-size: 15px;
  text-decoration: none;

  &:hover {
    cursor: pointer;
    color: #EEEEEE;
    transition: 0.5s;
  }
`
