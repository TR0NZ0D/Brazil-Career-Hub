import { FC, useState, useContext, FormEvent } from 'react';
import {
  Button,
  Container,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Modal,
  Radio,
  RadioGroup,
  TextField,
  Typography
} from '@mui/material';
import ErrorIcon from '@mui/icons-material/Error';
import { debounce } from 'lodash';
import FieldMasker from 'utilities/FieldMasker';
import GeneralValidator from 'utilities/GeneralValidator';
import CompanyAccount from 'models/Company/CompanyAccount';
import RegistrationStatuses from 'models/Company/RegistrationStatuses';
import LegalNatures from 'models/Company/LegalNatures';
import { createAccount } from 'api/company-requests/company-account-requests';
import { AuthContext } from 'contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';

const CompanyForm: FC = () => {

  const [companyAccount, setCompanyAccount] = useState<CompanyAccount>({
    registrationStatus: "1",
    legalNature: "EI"
  } as CompanyAccount);

  const { adminToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const [errorCreatingAccount, setErrorCreatingAccount] = useState<string>("");

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

  async function handleFormSubmit(e: any): Promise<void> {
    e.preventDefault();

    let response;

    try {
      let companyToSubmit: CompanyAccount = { ...companyAccount, cnpj: cnpj };
      response = await createAccount(companyToSubmit, adminToken!);

      if (response.status === 201) {
        navigate("/");
      }
    } catch (error: any) {
      console.log(error);
      setErrorCreatingAccount(error.response.data.message);
    }
  }

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
                onChange={(e) => {
                  setCompanyAccount({ ...companyAccount, registrationStatus: e.target.value as "1" | "2" | "3" | "4" | "5" | "8" })
                }}
              >
                {RegistrationStatuses.map(x => {
                  return (
                    <FormControlLabel key={x.key} value={x.key} control={< Radio />} label={x.description} />
                  )
                })}
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item lg={6} md={6} sm={12}>
            <FormControl>
              <FormLabel id="nature-group-label">Juridic Nature</FormLabel>
              <RadioGroup
                aria-labelledby="nature-radio-group"
                name="nature-radio-buttons-group"
                value={companyAccount.legalNature}
                onChange={(e) => setCompanyAccount({ ...companyAccount, legalNature: e.target.value as "EI" | "EIRELI" | "SI" | "LTDA" | "SA" | "SLU" })}
              >
                {LegalNatures.map(x => (
                  <FormControlLabel key={x.key} value={x.key} control={<Radio />} label={x.description} />
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
              type="number"
              fullWidth
              onChange={(e) => handleCnaeChange(e.target as HTMLInputElement)}
            />
          </Grid>

          {/* <Grid item sm={12} md={6} lg={6}>
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
          </Grid> */}

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