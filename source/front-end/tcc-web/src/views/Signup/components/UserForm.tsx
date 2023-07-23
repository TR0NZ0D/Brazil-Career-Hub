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
  Container,
  Modal
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
import { debounce } from 'lodash';

const UserForm: FC = () => {

  const [creatingAccount, setCreatingAccount] = useState<boolean>(false);
  const [errorCreatingAccount, setErrorCreatingAccount] = useState<string>("");
  const navigate = useNavigate();

  const { adminToken } = useContext(AuthContext);

  const [userName, setUserName] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");
  const [birthDate, setBirthDate] = useState<Dayjs | null>();
  const [gender, setGender] = useState<"NI" | "M" | "F" | "NB">("NI");
  const [cpf, setCpf] = useState<string>("");
  const [biography, setBiography] = useState<string | undefined>();
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

  useEffect(() => {
    setLanguagesColumn1(languages.slice(0, 31));
    setLanguagesColumn2(languages.slice(31, 62));
    setLanguagesColumn3(languages.slice(62, 93));
    setLanguagesColumn4(languages.slice(93, 123));
  }, [languages])

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
          const userProfile: UserProfile = new UserProfile(userName, languagesSpoken, gender, birthDate!,
            nationality, socialLife, biography, "", cpf, contactPhone, address);

          try {
            resp = await createUserProfile(userProfile, adminToken!);
            navigate("/");
          } catch (error: any) {
            await showErrorAndResetAccount(error!.response.data);
          }
        }

        else
          await showErrorAndResetAccount(resp!.data.message)
      }

      else
        setUserNameError("this username already exists")


    } catch (error: any) {
      setErrorCreatingAccount(error!.response.data.message)
    } finally {
      setCreatingAccount(false);
    }
  }

  async function showErrorAndResetAccount(error: any) {
    let errorMessage: string = "";
    Object.entries(error)
      .forEach(([key, value]) => {
        if (errorMessage === "")
          errorMessage = `[${key as string}: ${value as string}]`;

        else
          errorMessage += `, [${key as string}: ${value as string}]`;
      })
    setErrorCreatingAccount(errorMessage);
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

  function showHelperText(value: string, minChar: number): boolean {
    if (value === "" || value.length > minChar)
      return false;

    return true;
  }

  const handleInputChange = debounce((setFunction: (setVal: string) => void, element: HTMLInputElement, masker?: (text: string) => string) => {
    let value: string = element.value;

    if (masker) {
      value = masker(value)
      element.value = value;
    }

    setFunction(value);
  }, 100);

  return (
    <>
      <Modal open={errorCreatingAccount !== ""} onClose={() => setErrorCreatingAccount("")} >
        <Grid
          container
          item
          lg={5}
          md={8}
          sm={8}
          xs={10}
          display="flex"
          justifyContent="center"
          alignItems="center"
          style={{
            borderRadius: 10,
            backgroundColor: "#f7f6f6",
            padding: "5% 5%",
            margin: "5% auto",
          }}
        >
          <ErrorIcon style={{ fill: "#FAB91A", fontSize: 40, marginBottom: "3%" }} />
          <Typography gutterBottom>An error happened while creating your account: {errorCreatingAccount}</Typography>

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
      </Modal>

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

      {!creatingAccount &&
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
                variant="outlined"
                fullWidth
                onChange={(e) => {
                  handleInputChange(setUserName, e.target as HTMLInputElement)

                  if (e.target.value.length < 3)
                    setUserNameError("username must have at least 2 chars")

                  else
                    setUserNameError("")
                }}
                helperText={userNameError !== "" && userNameError}
                error={userName !== "" && userName.length < 3}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="name"
                label="Name"
                fullWidth
                onChange={(e) => handleInputChange(setName, e.target as HTMLInputElement)}
                helperText={showHelperText(name, 2) && "name must have at least 2 chars"}
                error={showHelperText(name, 2)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="surname"
                label="Surname"
                fullWidth
                onChange={(e) => handleInputChange(setSurname, e.target as HTMLInputElement)}
                helperText={showHelperText(surname, 2) && "surname must have at least 2 chars"}
                error={showHelperText(surname, 2)}
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
                  onChange={(e) => setGender(e.target.value as "NI" | "M" | "F" | "NB")}
                >
                  <FormControlLabel value="NI" control={<Radio />} label="I Prefer Not To Inform" />
                  <FormControlLabel value="M" control={<Radio />} label="Male" />
                  <FormControlLabel value="F" control={<Radio />} label="Female" />
                  <FormControlLabel value="NB" control={<Radio />} label="Non Binary" />
                </RadioGroup>
              </FormControl>
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="CPF"
                label="CPF"
                fullWidth
                onChange={(e) => {
                  e.target.value = FieldMasker.maskCpf(e.target.value);
                  handleInputChange(setCpf, e.target as HTMLInputElement)
                }}
                helperText={cpf !== "" && !GeneralValidator.validateCpf(cpf) && "Type a valid CPF"}
                error={cpf !== "" && !GeneralValidator.validateCpf(cpf)}
                inputProps={{ maxLength: 14 }}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                required
                id="email"
                label="E-mail"
                type="email"
                fullWidth
                onChange={(e) => handleInputChange(setEmail, e.target as HTMLInputElement)}
                helperText={email !== "" && !GeneralValidator.validateEmail(email) && "type a valid e-mail"}
                error={email !== "" && !GeneralValidator.validateEmail(email)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="address"
                label="Address"
                fullWidth
                onChange={(e) => handleInputChange(setAddress, e.target as HTMLInputElement)}
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

            <Grid item lg={12} md={12} sm={12}>
              <TextField
                id="biography"
                label="Write your biography"
                fullWidth
                multiline
                rows={10}
                onChange={(e) => handleInputChange(setBiography, e.target as HTMLInputElement)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="linkedin"
                label="Linkedin"
                fullWidth
                onChange={(e) => handleInputChange(setLinkedin, e.target as HTMLInputElement)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="website"
                label="Website"
                fullWidth
                onChange={(e) => handleInputChange(setWebsite, e.target as HTMLInputElement)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="instagram"
                label="Instagram"
                fullWidth
                onChange={(e) => handleInputChange(setInstagram, e.target as HTMLInputElement)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="facebook"
                label="Facebook"
                fullWidth
                onChange={(e) => handleInputChange(setFacebook, e.target as HTMLInputElement)}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="twitter"
                label="Twitter"
                fullWidth
                onChange={(e) => handleInputChange(setTwitter, e.target as HTMLInputElement)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="cellphone"
                label="Contact phone"
                fullWidth
                onChange={(e) => handleInputChange(setContactPhone, e.target as HTMLInputElement)}
              />
            </Grid>

            <Grid item lg={6} md={6} sm={12}>
              <TextField
                id="password"
                label="Password"
                type="password"
                required
                fullWidth
                onChange={(e) => handleInputChange(setPassword, e.target as HTMLInputElement)}
                helperText={showHelperText(password, 5) && "Your password must contain at least 5 chars"}
                error={showHelperText(password, 5)}
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