import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';

const CompanyForm: FC = () => {

  const [cnpj, setCnpj] = useState<string>("");
  const [socialReason, setSocialReason] = useState<string>("");
  const [registrationStatus, setRegistrationStatus] = useState<string>("");
  const [fantasyName, setFantasyName] = useState<string>("");
  const [economicActivity, setEconomicActivity] = useState<string>("");
  const [juridicNature, setJuridicNature] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [contact, setContact] = useState<string>("");
  const [businesStartedDate, setBusinessStartedDate] = useState<string>("");
  const [capital, setCapital] = useState<string>("");
  const [employeeQuantity, setEmployeeQuantity] = useState<string>("");
  const [website, setWebsite] = useState<string>("");
  const [socialMedia, setSocialMedia] = useState<string>("");

  return (
    <>
      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="CNPJ"
          label="CNPJ"
          fullWidth
          value={cnpj}
          onChange={(e) => setCnpj(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="social-reason"
          label="Social Reason"
          fullWidth
          value={socialReason}
          onChange={(e) => setSocialReason(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="registration-status"
          label="Situação Cadastral"
          fullWidth
          value={registrationStatus}
          onChange={(e) => setRegistrationStatus(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="fantasy-name"
          label="Nome Fantasia"
          fullWidth
          value={fantasyName}
          onChange={(e) => setFantasyName(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="economic-activity"
          label="Atividade Economica"
          fullWidth
          value={economicActivity}
          onChange={(e) => setEconomicActivity(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="juridic-natura"
          label="Natureza Juridica"
          fullWidth
          value={juridicNature}
          onChange={(e) => setJuridicNature(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="address"
          label="Address"
          fullWidth
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="contact"
          label="Contact"
          fullWidth
          value={contact}
          onChange={(e) => setContact(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="business-started-year"
          label="Business Started Year"
          type="number"
          fullWidth
          value={businesStartedDate}
          onChange={(e) => setBusinessStartedDate(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="capital"
          label="Capital"
          type="number"
          fullWidth
          value={capital}
          onChange={(e) => setCapital(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="employee-quantity"
          label="Employee quantity"
          type="number"
          fullWidth
          value={employeeQuantity}
          onChange={(e) => setEmployeeQuantity(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="website"
          label="Website"
          fullWidth
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
        />
      </Grid>

      <Grid item sm={12} md={6} lg={6}>
        <TextField
          required
          id="social-media"
          label="Social Media"
          fullWidth
          value={socialMedia}
          onChange={(e) => setSocialMedia(e.target.value)}
        />
      </Grid>
    </>
  )
}

export default CompanyForm;