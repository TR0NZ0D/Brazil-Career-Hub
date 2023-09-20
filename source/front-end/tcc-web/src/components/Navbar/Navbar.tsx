import { FC, useContext } from 'react';
import { LinkMenu, Nav, OptionGrid } from './styles';
import { AuthContext } from 'contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button, Grid } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';

const Navbar: FC = () => {
  const navigate = useNavigate();
  const { entityType, logout } = useContext(AuthContext);

  function isActive(path: string): boolean {
    if (window.location.pathname === path) {
      return true;
    }

    return false;
  }

  function handleLogoutClick(): void {
    logout();
    navigate("/login");
  }

  const userRoutes = [
    { route: "/", text: "Jobs" },
    { route: "/myresumes", text: "Resumes" },
  ]

  return (
    <Nav container display="flex" justifyContent="space-between">
      {entityType === "user" &&
        <Grid container item display="flex" style={{ padding: "0 2%" }} lg={6} spacing={1}>
          {userRoutes.map(x => (
            <OptionGrid
              key={x.route}
              container
              item
              lg={2}
              display="flex"
              alignItems="center"
              justifyContent="center"
              className={isActive(x.route) ? "active" : ""}>
              <LinkMenu onClick={() => navigate(x.route)}>{x.text}</LinkMenu>
            </OptionGrid>
          ))}
        </Grid>}

      <Grid container item display="flex" lg={6} justifyContent="flex-end" alignItems="center">
        <Grid item>
          <Button
            variant="contained"
            endIcon={<LogoutIcon />}
            style={{ backgroundColor: "transparent" }}
            onClick={handleLogoutClick}
          >
            Logout
          </Button>
        </Grid>
      </Grid>
    </Nav>
  )
}

export default Navbar;