import { FC } from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';

const CompanyForm: FC = () => {
  return (
    <>
      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="CNPJ"
          label="CNPJ"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="social-reason"
          label="Social Reason"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="registration-status"
          label="Situação Cadastral"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="fantasy-name"
          label="Nome Fantasia"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="economic-activity"
          label="Atividade Economica"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="juridic-natura"
          label="Natureza Juridica"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="address"
          label="Address"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="contact"
          label="Contact"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="business-started-year"
          label="Business Started Year"
          type="number"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="capital"
          label="Capital"
          type="number"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="employee-quantity"
          label="Employee quantity"
          type="number"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="website"
          label="Website"
          fullWidth
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="social-media"
          label="Social Media"
          fullWidth
        />
      </Grid>
    </>
  )
}

export default CompanyForm;