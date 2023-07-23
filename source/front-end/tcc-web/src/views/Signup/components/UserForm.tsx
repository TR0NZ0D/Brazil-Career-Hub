import { FC, useState, useEffect, useContext } from 'react';
import ErrorIcon from '@mui/icons-material/Error';
import { AuthContext } from 'contexts/AuthContext';
import FieldMasker from 'utilities/FieldMasker';
import GeneralValidator from 'utilities/GeneralValidator';
import { languages, nationalities } from 'utilities/RelevantData';
import {
  Button,
  Checkbox,
  FormGroup,
  InputLabel,
  MenuItem, Select,
  Typography,
  Radio,
  RadioGroup,
  FormLabel,
  FormControlLabel,
  FormControl,
  TextField,
  Grid,
  CircularProgress,
  Container
} from '@mui/material';
import UserAccount from 'models/User/UserAccount';
import { createUserAccount, deleteUserAccount, getUserAccount } from 'api/users/user-account-requests';
import { createUserProfile } from 'api/users/user-profile-requests';
import SocialAccount from 'models/User/SocialAccount';
import UserProfile from 'models/User/UserProfile';
import { useNavigate } from 'react-router-dom';
import { AxiosResponse } from 'axios';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs, { Dayjs } from 'dayjs';

const UserForm: FC = () => {

  const [creatingAccount, setCreatingAccount] = useState<boolean>(false);
  const [errorCreatingAccount, setErrorCreatingAccount] = useState<string>("");
  const navigate = useNavigate();

  const { adminToken } = useContext(AuthContext);

  const [userName, setUserName] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");
  const [birthDate, setBirthDate] = useState<Dayjs | null>();
  const [gender, setGender] = useState<string>("");
  const [cpf, setCpf] = useState<string>("");
  const [nationality, setNationality] = useState<string>("");
  const [languagesSpoken, setLanguagesSpoken] = useState<string[]>([]);
  const [email, setEmail] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [linkedin, setLinkedin] = useState<string | undefined>(undefined);
  const [website, setWebsite] = useState<string | undefined>(undefined);
  const [instagram, setInstagram] = useState<string | undefined>(undefined);
  const [facebook, setFacebook] = useState<string | undefined>(undefined);
  const [twitter, setTwitter] = useState<string | undefined>(undefined);
  const [contactPhone, setContactPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [languagesColumn1, setLanguagesColumn1] = useState<string[]>([]);
  const [languagesColumn2, setLanguagesColumn2] = useState<string[]>([]);
  const [languagesColumn3, setLanguagesColumn3] = useState<string[]>([]);
  const [languagesColumn4, setLanguagesColumn4] = useState<string[]>([]);

  const [userNameError, setUserNameError] = useState<string>("");
  const [ageError, setAgeError] = useState<string>("");
  const [nameError, setNameError] = useState<boolean>(false);
  const [surnameError, setSurnameError] = useState<boolean>(false);
  const [cpfError, setCpfError] = useState<boolean>(false);
  const [emailError, setEmailError] = useState<boolean>(false);
  const [passwordError, setPasswordError] = useState<boolean>(false);

  console.log(`${new Date().getFullYear() - 18}-${new Date().getMonth() + 1}-${new Date().getDate()}`);

  useEffect(() => {
    setLanguagesColumn1(languages.slice(0, 31));
    setLanguagesColumn2(languages.slice(31, 62));
    setLanguagesColumn3(languages.slice(62, 93));
    setLanguagesColumn4(languages.slice(93, 123));
  }, [languages])

  function handleNotEmptyFieldsChange(val: string, setErrorCallback: (setVal: boolean) => void, minChar: number = 2): void {
    if (val === undefined || val === null || val.length < minChar)
      setErrorCallback(true);

    else
      setErrorCallback(false);
  }

  function handleLanguagesChange(val: string) {
    if (languagesSpoken.includes(val)) {
      let newLanguages: string[] = languagesSpoken.filter(x => x !== val);
      setLanguagesSpoken(newLanguages);
    }

    else
      setLanguagesSpoken([...languagesSpoken, val]);
  }

  async function handleFormSubmit(e: any) {
    e.preventDefault();
    handleCreateUserAccount();
  }

  async function handleCreateUserAccount() {
    try {
      setCreatingAccount(true);

      let resp: AxiosResponse | undefined = undefined;
      const userAcExists = await userAccountExists(userName!);

      if (!userAcExists) {
        const user: UserAccount = new UserAccount(userName, password, name, surname, email);
        resp = await createUserAccount(user, adminToken!);

        if (resp.status === 201) {
          const socialLife: SocialAccount = new SocialAccount(linkedin, twitter,
            facebook, instagram, website);
          const userProfile: UserProfile = new UserProfile(userName, languages, "NI", birthDate!,
            nationality, socialLife);

          try {
            resp = await createUserProfile(userProfile, adminToken!);
            navigate("/");
          } catch (error: any) {
            await showErrorAndResetAccount(error!.response.data.message);
          }
        }

        else
          await showErrorAndResetAccount(resp!.data.message)
      }

      else
        setUserNameError("this username already exists")


    } catch (error: any) {
      console.log(error);
      setErrorCreatingAccount(error!.response.data.message)
    } finally {
      setCreatingAccount(false);
    }
  }

  async function showErrorAndResetAccount(error: string) {
    setErrorCreatingAccount(error);
    await deleteUserAccount(userName, adminToken!);
  }

  async function userAccountExists(username: string) {
    try {
      const response = await getUserAccount(username, adminToken!);
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }

  return (
    <>
      {creatingAccount &&
        <Grid container justifyContent="center" alignItems="center" display="flex">
          <Grid
            container
            item
            xs={8}
            md={8}
            sm={8}
            display="flex"
            justifyContent="center"
            alignItems="center"
          >
            <Container
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                flexDirection: "column",
                borderRadius: 10,
                margin: "5% auto",
                padding: "12%"
              }}
            >
              <CircularProgress />
              <Typography>Creating your account...</Typography>
            </Container>
          </Grid>
        </Grid>
      }

      {errorCreatingAccount !== "" &&
        <Grid container justifyContent="center" alignItems="center" display="flex">
          <Grid
            container
            item
            xs={8}
            md={8}
            sm={8}
            display="flex"
            justifyContent="center"
            alignItems="center"
            style={{
              borderRadius: 10,
              backgroundColor: "#f7f6f6",
              padding: "5% 13%",
              margin: "5% auto"
            }}
          >

            <ErrorIcon style={{ fill: "#FAB91A", fontSize: 40, marginBottom: "3%" }} />
            <Typography gutterBottom>An error happened while creating your account: {errorCreatingAccount}...</Typography>

            <Grid
              container
              item
              display="flex"
              style={{
                marginTop: "2%"
              }}
            >
              <Button
                variant='contained'
                color="primary"
                style={{ marginRight: "2%" }}
                onClick={(e) => handleFormSubmit(e)}
              >
                Retry
              </Button>
              <Button
                variant='outlined'
                onClick={() => setErrorCreatingAccount("")}
              >
                Cancel
              </Button>
            </Grid>
          </Grid>
        </Grid>
      }

      {!creatingAccount && errorCreatingAccount === "" &&
        <Container style={{ padding: "4% 4% 4% 4%" }}>

          <Grid container spacing={2} component="form" onSubmit={(e) => handleFormSubmit(e)}>
            <Grid item lg={12} md={12} sm={12}>
              <Typography
                variant="h5"
                gutterBottom
                style={{
                  marginBottom: "3%",
                  fontWeight: "bolder"
                }}
              >
                Sign Up
              </Typography>
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="username"
                label="Username"
                fullWidth
                value={userName}
                onChange={(e) => {
                  const text: string = e.target.value;
                  setUserName(text);

                  if (text.length <= 2)
                    setUserNameError("username must have at least 2 chars");

                  else
                    setUserNameError("");
                }}
                helperText={userNameError}
                error={userNameError !== ""}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="name"
                label="Name"
                fullWidth
                value={name}
                onChange={(e) => {
                  const text: string = e.target.value;
                  setName(text);
                  handleNotEmptyFieldsChange(text, setNameError);
                }}
                helperText={nameError ? "name must have at least 2 chars" : ""}
                error={nameError}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="surname"
                label="Surname"
                fullWidth
                value={surname}
                onChange={(e) => {
                  const text: string = e.target.value;
                  setSurname(text);
                  handleNotEmptyFieldsChange(text, setSurnameError);
                }}
                helperText={surnameError ? "surname must have at least 2 chars" : ""}
                error={surnameError}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <DatePicker
                label="Select your birth date"
                maxDate={dayjs(`${new Date().getFullYear() - 18}-${new Date().getMonth() + 1}-${new Date().getDate()}`)}
                slotProps={{
                  textField: {
                    required: true,
                    fullWidth: true
                  }
                }}
                onChange={(e: Dayjs | null) => setBirthDate(e)} />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <FormControl>
                <FormLabel id="sex-group-label">Gender</FormLabel>
                <RadioGroup
                  aria-labelledby="sex-radio-group"
                  defaultValue="Male"
                  name="sex-radio-buttons-group"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  <FormControlLabel value="Female" control={<Radio />} label="Female" />
                  <FormControlLabel value="Male" control={<Radio />} label="Male" />
                  <FormControlLabel value="Other" control={<Radio />} label="Other" />
                </RadioGroup>
              </FormControl>
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="CPF"
                label="CPF"
                fullWidth
                value={cpf}
                onChange={(e) => {
                  const text: string = FieldMasker.maskCpf(e.target.value);
                  setCpf(text);
                  setCpfError(!GeneralValidator.validateCpf(text));
                }}
                error={cpfError}
                helperText={cpfError ? "type a valid CPF" : ""}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="email"
                label="E-mail"
                type="email"
                fullWidth
                value={email}
                onChange={(e) => {
                  const text: string = e.target.value;
                  setEmailError(!GeneralValidator.validateEmail(text));
                  setEmail(e.target.value);
                }}
                error={emailError}
                helperText={emailError ? "type a valid e-mail" : ""}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="address"
                label="Address"
                fullWidth
                value={address}
                onChange={(e) => setAddress(e.target.value)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <FormControl fullWidth required>
                <InputLabel id="nationality-select-label">Nationality</InputLabel>
                <Select
                  labelId="nationality-select-label"
                  id="nationality-select"
                  value={nationality}
                  label="Nationality"
                  onChange={(e) => setNationality(e.target.value)}
                >
                  {nationalities.map(x => {
                    return (
                      <MenuItem key={x} value={x}>{x}</MenuItem>
                    )
                  })}
                </Select>
              </FormControl>
            </Grid>

            <Grid item lg={12} md={12} sm={12}>
              <Typography variant="h6" gutterBottom>Select your languages:</Typography>
            </Grid>

            <Grid item lg={3} md={3} sm={6}>
              <FormGroup>
                {languagesColumn1.map(x => {
                  return (
                    <FormControlLabel
                      key={x}
                      control={<Checkbox />}
                      label={x}
                      onChange={() => handleLanguagesChange(x)}
                    ></FormControlLabel>
                  )
                })}
              </FormGroup>
            </Grid>

            <Grid item lg={3} md={3} sm={6}>
              <FormGroup>
                {languagesColumn2.map(x => {
                  return (
                    <FormControlLabel
                      key={x}
                      control={<Checkbox />}
                      label={x}
                      onChange={() => handleLanguagesChange(x)}
                    ></FormControlLabel>
                  )
                })}
              </FormGroup>
            </Grid>

            <Grid item lg={3} md={3} sm={6}>
              <FormGroup>
                {languagesColumn3.map(x => {
                  return (
                    <FormControlLabel
                      key={x}
                      control={<Checkbox />}
                      label={x}
                      onChange={() => handleLanguagesChange(x)}
                    ></FormControlLabel>
                  )
                })}
              </FormGroup>
            </Grid>

            <Grid item lg={3} md={3} sm={6}>
              <FormGroup>
                {languagesColumn4.map(x => {
                  return (
                    <FormControlLabel
                      key={x}
                      control={<Checkbox />}
                      label={x}
                      onChange={() => handleLanguagesChange(x)}
                    ></FormControlLabel>
                  )
                })}
              </FormGroup>
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="linkedin"
                label="Linkedin"
                fullWidth
                value={linkedin}
                onChange={(e) => setLinkedin(e.target.value)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="website"
                label="Website"
                fullWidth
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="instagram"
                label="Instagram"
                fullWidth
                value={instagram}
                onChange={(e) => setInstagram(e.target.value)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="facebook"
                label="Facebook"
                fullWidth
                value={facebook}
                onChange={(e) => setFacebook(e.target.value)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="twitter"
                label="Twitter"
                fullWidth
                value={twitter}
                onChange={(e) => setTwitter(e.target.value)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="cellphone"
                label="Contact phone"
                fullWidth
                value={contactPhone}
                onChange={(e) => setContactPhone(e.target.value)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="password"
                label="Password"
                type="password"
                required
                fullWidth
                value={password}
                onChange={(e) => {
                  const text: string = e.target.value;
                  handleNotEmptyFieldsChange(text, setPasswordError, 5);
                  setPassword(e.target.value)
                }}
                error={passwordError}
                helperText={passwordError ? "Your password must contain at least 5 chars" : ""}
              />
            </Grid>

            <Grid container item justifyContent="flex-end">
              <Grid item>
                <Button variant="contained" type="submit">Submit</Button>
              </Grid>
            </Grid>
          </Grid>
        </Container>

      }
    </>
  )
}

export default UserForm;