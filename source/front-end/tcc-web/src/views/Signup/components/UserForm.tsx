import { FC, FormEvent, useState, useEffect } from 'react';
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
  Grid
} from '@mui/material';

interface Props {
  onSubmit: (
    userName: string,
    name: string,
    surname: string,
    age: number,
    gender: string,
    cpf: string,
    email: string,
    address: string,
    nationality: string,
    languages: string[],
    portfolio: string,
    socialMedia: string,
    contact: string,
    password: string) => void
}

const UserForm: FC<Props> = ({ onSubmit }: Props) => {

  const [userName, setUserName] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");
  const [age, setAge] = useState<number | string>("");
  const [gender, setGender] = useState<string>("");
  const [cpf, setCpf] = useState<string>("");
  const [nationality, setNationality] = useState<string>("");
  const [languagesSpoken, setLanguagesSpoken] = useState<string[]>([]);
  const [email, setEmail] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [portfolio, setPortfolio] = useState<string>("");
  const [socialMedia, setSocialMedia] = useState<string>("");
  const [contactPhone, setContactPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [languagesColumn1, setLanguagesColumn1] = useState<string[]>([]);
  const [languagesColumn2, setLanguagesColumn2] = useState<string[]>([]);
  const [languagesColumn3, setLanguagesColumn3] = useState<string[]>([]);
  const [languagesColumn4, setLanguagesColumn4] = useState<string[]>([]);

  const [userNameError, setUserNameError] = useState<boolean>(false);
  const [nameError, setNameError] = useState<boolean>(false);
  const [surnameError, setSurnameError] = useState<boolean>(false);
  const [cpfError, setCpfError] = useState<boolean>(false);
  const [emailError, setEmailError] = useState<boolean>(false);
  const [passwordError, setPasswordError] = useState<boolean>(false);

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

  async function handleFormSubmit(e: FormEvent) {
    e.preventDefault();
    onSubmit(userName, name, surname, age as number, gender, cpf,
      email, address, nationality, languages,
      portfolio, socialMedia, contactPhone, password);
  }

  return (
    <Grid container spacing={2} component="form" onSubmit={(e) => handleFormSubmit(e)}>
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
          onChange={(e) => {
            if (e.target.value === "")
              setAge("");

            else
              setAge(Number.parseInt(e.target.value))
          }}
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
        <FormControl fullWidth>
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

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="password"
          label="Password"
          fullWidth
          type="password"
          value={password}
          onChange={(e) => {
            const text: string = e.target.value;
            handleNotEmptyFieldsChange(text, setPasswordError, 5);
            setPassword(e.target.value)
          }}
          helperText={passwordError ? "Your password must contain at least 5 chars" : ""}
        />
      </Grid>

      <Grid container item justifyContent="flex-end">
        <Grid item>
          <Button variant="contained" type="submit">Submit</Button>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default UserForm;