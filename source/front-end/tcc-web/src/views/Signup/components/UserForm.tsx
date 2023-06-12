import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FieldMasker from '../../../utilities/FieldMasker';
import GeneralValidator from '../../../utilities/GeneralValidator';
import { languages } from '../../../utilities/RelevantData';

const UserForm: FC = () => {

  const [userName, setUserName] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");
  const [age, setAge] = useState<number>(18);
  const [gender, setGender] = useState<string>("");
  const [cpf, setCpf] = useState<string>("");
  const [numberOfJobRegistration, setNumberOfJobRegistration] = useState<number>(0);
  const [email, setEmail] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [portfolio, setPortfolio] = useState<string>("");
  const [socialMedia, setSocialMedia] = useState<string>("");
  const [contactPhone, setContactPhone] = useState<string>("");

  const [userNameError, setUserNameError] = useState<boolean>(false);
  const [nameError, setNameError] = useState<boolean>(false);
  const [surnameError, setSurnameError] = useState<boolean>(false);
  const [cpfError, setCpfError] = useState<boolean>(false);
  const [numberOfJobRegistrationError, setNumberOfJobRegistrationError] = useState<boolean>(false);
  const [emailError, setEmailError] = useState<boolean>(false);

  function handleNotEmptyFieldsChange(val: string, setErrorCallback: (setVal: boolean) => void, minChar: number = 2) {
    if (val === undefined || val === null || val.length < minChar)
      setErrorCallback(true);

    else
      setErrorCallback(false);
  }

  return (
    <>
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
            handleNotEmptyFieldsChange(text, setUserNameError);
          }}
          helperText={userNameError ? "username must have at least 2 chars" : ""}
          error={userNameError}
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
        <TextField
          required
          id="age"
          label="Age"
          type="number"
          fullWidth
          value={age}
          onChange={(e) => setAge(Number.parseInt(e.target.value))}
        />
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
          id="job-id"
          label="Number of your job registration"
          fullWidth
          value={numberOfJobRegistration}
          onChange={(e) => setNumberOfJobRegistration(Number.parseInt(e.target.value))}
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

      {/* Todo: Add nationality */}

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="address"
          label="Address"
          fullWidth
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
      </Grid>

      {/* Todo: Add languages */}

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="portfolio"
          label="Website for your portfolio"
          fullWidth
          value={portfolio}
          onChange={(e) => setPortfolio(e.target.value)}
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="social-media"
          label="Social media"
          fullWidth
          value={socialMedia}
          onChange={(e) => setSocialMedia(e.target.value)}
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
    </>
  )
}

export default UserForm;