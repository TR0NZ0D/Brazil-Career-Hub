import { FC, useState } from 'react';
import {
  Button,
  Container,
  Grid,
  TextField,
  Typography
} from '@mui/material';
import { debounce } from 'lodash';
import FieldMasker from 'utilities/FieldMasker';
import GeneralValidator from 'utilities/GeneralValidator';

const CompanyForm: FC = () => {

  const [cnpj, setCnpj] = useState<string>("");
  const [corporateName, setCorporateName] = useState<string>("");
  const [registrationStatus, setRegistrationStatus] = useState<string>("");
  const [fantasyName, setFantasyName] = useState<string>("");
  const [cnae, setCnae] = useState<string>("")
  const [economicActivity, setEconomicActivity] = useState<string>("");
  const [juridicNature, setJuridicNature] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [contact, setContact] = useState<string>("");
  const [businesStartedDate, setBusinessStartedDate] = useState<string>("");
  const [capital, setCapital] = useState<string>("");
  const [employeeQuantity, setEmployeeQuantity] = useState<string>("");
  const [website, setWebsite] = useState<string>("");
  const [socialMedia, setSocialMedia] = useState<string>("");

  const handleCnpjChange = debounce((element: HTMLInputElement) => {

  });

  const handleCorporateNameChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    setCorporateName(val);
  }, 350);

  const handleRegistrationStatusChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    setRegistrationStatus(val);
  }, 350);

  const handleFantasyNameChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    setFantasyName(val);
  }, 350);

  const handleCnaeChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    setCnae(val);
  }, 350);

  const handleLegalNatureChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    setRegistrationStatus(val);
  }, 350);

  return (
    <>
      <Container style={{ padding: "4% 4% 4% 4%" }}>
        <Grid container spacing={2} component="form">
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

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              required
              id="CNPJ"
              label="CNPJ"
              variant="outlined"
              fullWidth
              inputProps={{ maxLength: 18 }}
              onChange={(e) => {
                let value = FieldMasker.maskCnpj(e.target.value);
                e.target.value = value;
                setCnpj(value);
              }}
              helperText={cnpj !== "" && !GeneralValidator.validateCnpj(cnpj) && "Please type a valid CNPJ"}
              error={cnpj !== "" && !GeneralValidator.validateCnpj(cnpj)}
            />
          </Grid>

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              required
              id="corporate-name"
              label="Razão social"
              fullWidth
              onChange={(e) => handleCorporateNameChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              required
              id="registration-status"
              label="Situação Cadastral"
              fullWidth
              onChange={(e) => handleRegistrationStatusChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              required
              id="fantasy-name"
              label="Fantasy name"
              fullWidth
              onChange={(e) => handleFantasyNameChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              required
              id="cnae"
              label="Cnae"
              fullWidth
              onChange={(e) => handleCnaeChange(e.target as HTMLInputElement)}
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

          <Grid container item justifyContent="flex-end">
            <Grid item>
              <Button variant="contained" type="submit">Submit</Button>
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </>
  )
}

export default CompanyForm;