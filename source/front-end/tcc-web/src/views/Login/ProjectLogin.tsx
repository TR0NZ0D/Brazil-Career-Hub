import {
  Button,
  FormControl,
  FormControlLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField
} from '@mui/material'
import LogoImage from 'assets/images/logo.png';
import { LinkToSignup, LoginContainer, LoginTitle, Logo } from './styles';
import { useState, useContext } from 'react';
import { AuthContext } from 'contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import FieldMasker from 'utilities/FieldMasker';

const Login = () => {

  const [username, setUsername] = useState<string>("");
  const [cnpj, setCnpj] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [userType, setUserType] = useState<"company" | "user">("user");

  const { userLogin, companyLogin } = useContext(AuthContext);

  const navigate = useNavigate();

  async function handleLoginSubmit(e: any) {
    e.preventDefault();

    let entity;
    if (userType === "user")
      entity = await userLogin(username, password);
    else
      entity = await companyLogin(cnpj, password);

    if (entity !== undefined) {
      navigate("/");
    }

    else
      alert("Invalid login");
  }

  return (
    <Grid container display="flex" alignItems="center" justifyContent="center" flexDirection="column">
      <Logo src={LogoImage} alt="logo" />

      <LoginContainer onSubmit={handleLoginSubmit}>
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
                value={userType}
                onChange={(e) => setUserType(e.target.value as "company" | "user")}
              >
                <FormControlLabel value="user" control={<Radio />} label="I am a user" />
                <FormControlLabel value="company" control={<Radio />} label="I am a company" />
              </RadioGroup>
            </FormControl>
          </Grid>
        </Grid>

        <Grid item container display="flex" flexDirection="column" justifyContent="space-between" alignItems="flex-start">

          {userType === "user" &&
            <TextField
              id="user-text"
              label="Username"
              variant="outlined"
              required
              fullWidth
              style={{ marginBottom: "5%" }}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />}

          {userType === "company" &&
            <TextField
              id="cnpj-text"
              label="CNPJ"
              variant="outlined"
              required
              fullWidth
              inputProps={{ maxLength: 18 }}
              style={{ marginBottom: "5%" }}
              value={cnpj}
              onChange={(e) => setCnpj(FieldMasker.maskCnpj(e.target.value))}
            />}

          <TextField
            id="password-input"
            label="Password"
            variant="outlined"
            type="password"
            required
            fullWidth
            style={{ marginBottom: "5%" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Grid>

        <Grid item container justifyContent="flex-end" alignItems="center" style={{ gap: "6%" }}>
          <LinkToSignup to="/signup">Don't you have an account yet?</LinkToSignup>
          <Button variant="contained" type="submit" style={{ width: "15%" }}>Login</Button>
        </Grid>
      </LoginContainer>
    </Grid>
  )
}

export default Login