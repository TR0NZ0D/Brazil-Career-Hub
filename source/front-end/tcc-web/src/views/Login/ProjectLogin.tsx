import { FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField, Typography } from '@mui/material'
import LogoImage from 'assets/images/logo.png';
import { LoginContainer, LoginTitle, Logo } from './styles';

const Login = () => {
  return (
    <Grid container display="flex" alignItems="center" justifyContent="center" flexDirection="column">
      <Logo src={LogoImage} alt="logo" />

      <LoginContainer>
        <Grid container item lg={12} md={12} sm={12} style={{ marginBottom: "5%" }}>
          <Grid container item lg={6} md={6} sm={6}>
            <LoginTitle variant="h5" gutterBottom>Login</LoginTitle>
          </Grid>
          <Grid container item lg={6} md={6} sm={6} display="flex" justifyContent="flex-end" alignItems="center">
            <FormControl>
              <RadioGroup
                row
                aria-labelledby="type-radio-buttons"
                name="type-radio-buttons-group"
              >
                <FormControlLabel value="user" control={<Radio />} label="I am a user" />
                <FormControlLabel value="company" control={<Radio />} label="I am a company" />
              </RadioGroup>
            </FormControl>
          </Grid>
        </Grid>

        <Grid item container display="flex" flexDirection="column" justifyContent="space-between" alignItems="flex-start">
          <TextField id="user-text" label="Username" variant="outlined" />
          <TextField id="password-input" label="Password" variant="outlined" />
        </Grid>
      </LoginContainer>
    </Grid>
  )
}

export default Login