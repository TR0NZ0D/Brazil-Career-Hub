import { FC, useState } from 'react';
import {
  Button,
  Container,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField,
  Typography
} from '@mui/material';
import { debounce } from 'lodash';
import FieldMasker from 'utilities/FieldMasker';
import GeneralValidator from 'utilities/GeneralValidator';
import CompanyAccount from 'models/Company/CompanyAccount';
import RegistrationStatuses from 'models/Company/RegistrationStatuses';
import LegalNatures from 'models/Company/LegalNatures';

const CompanyForm: FC = () => {

  const [companyAccount, setCompanyAccount] = useState<CompanyAccount>({} as CompanyAccount);

  const [cnpj, setCnpj] = useState<string>("");
  const [economicActivity, setEconomicActivity] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [contact, setContact] = useState<string>("");
  const [businesStartedDate, setBusinessStartedDate] = useState<string>("");
  const [capital, setCapital] = useState<string>("");
  const [employeeQuantity, setEmployeeQuantity] = useState<string>("");
  const [website, setWebsite] = useState<string>("");
  const [socialMedia, setSocialMedia] = useState<string>("");

  const handleCorporateNameChange = debounce((element: HTMLInputElement) => {
    const val = element.value;
    const newCompany = { ...companyAccount, corporateName: val };
    setCompanyAccount(newCompany);
  }, 350);

  const handleFantasyNameChange = debounce((element: HTMLInputElement) => {
    setCompanyAccount({ ...companyAccount, fantasyName: element.value });
  }, 350);

  const handleCnaeChange = debounce((element: HTMLInputElement) => {
    setCompanyAccount({ ...companyAccount, cnae: element.value });
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

          <Grid item lg={6} md={6} sm={12}>
            <FormControl>
              <FormLabel id="registration-group-label">Registration Status</FormLabel>
              <RadioGroup
                aria-labelledby="registration-radio-group"
                defaultValue="None"
                name="registration-radio-buttons-group"
                value={companyAccount.registrationStatus}
                onChange={(e) => setCompanyAccount({ ...companyAccount, registrationStatus: e.target.value as "None" | "Active" | "Suspended" | "Inapt" | "Active not regular" | "Extinct" })}
              >
                {RegistrationStatuses.map(x => (
                  <FormControlLabel key={x.key} value={x.description} control={<Radio />} label={x.description} />
                ))}
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item lg={6} md={6} sm={12}>
            <FormControl>
              <FormLabel id="nature-group-label">Juridic Nature</FormLabel>
              <RadioGroup
                aria-labelledby="nature-radio-group"
                defaultValue="None"
                name="nature-radio-buttons-group"
                value={companyAccount.registrationStatus}
                onChange={(e) => setCompanyAccount({ ...companyAccount, legalNature: e.target.value as "Individual Entrepreneur (EI)" | "Individual Limited Liability Company (EIRELI)" | "Simple Society (SI)" | "Private Limited Company (LTDA)" | "Limited Liability Company (SA)" | "Single-Member Limited Company (SLU)" })}
              >
                {LegalNatures.map(x => (
                  <FormControlLabel key={x.key} value={x.description} control={<Radio />} label={x.description} />
                ))}
              </RadioGroup>
            </FormControl>
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