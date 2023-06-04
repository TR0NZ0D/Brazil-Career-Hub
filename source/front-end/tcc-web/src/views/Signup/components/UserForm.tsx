import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import { maskCpf } from '../../../utilities/field-mask';

const UserForm: FC = () => {

  const [cpf, setCpf] = useState<string>("");

  return (
    <>
      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="username"
          label="Username"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="name"
          label="Name"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="surname"
          label="Surname"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="age"
          label="Age"
          type="number"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <FormControl>
          <FormLabel id="sex-group-label">Gender</FormLabel>
          <RadioGroup
            aria-labelledby="sex-radio-group"
            defaultValue="Male"
            name="sex-radio-buttons-group"
          >
            <FormControlLabel value="female" control={<Radio />} label="Female" />
            <FormControlLabel value="male" control={<Radio />} label="Male" />
            <FormControlLabel value="other" control={<Radio />} label="Other" />
          </RadioGroup>
        </FormControl>
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="CPF"
          label="CPF"
          fullWidth
          value={cpf}
          onChange={(e) => setCpf(maskCpf(e.target.value))}
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="job-id"
          label="Number of your job registration"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="email"
          label="E-mail"
          type="email"
          fullWidth
        />
      </Grid>

      {/* Todo: Add nationality */}

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          required
          id="address"
          label="Address"
          fullWidth
        />
      </Grid>

      {/* Todo: Add languages */}

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="portfolio"
          label="Website for your portfolio"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="social-media"
          label="Social media"
          fullWidth
        />
      </Grid>

      <Grid item lg={6} md={6} sm={12}>
        <TextField
          id="cellphone"
          label="Contact phone"
          fullWidth
        />
      </Grid>
    </>
  )
}

export default UserForm;