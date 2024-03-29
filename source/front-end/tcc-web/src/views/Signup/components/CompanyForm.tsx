import { FC, useState, useContext, Fragment } from 'react';
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
import CompanyProfile, { addItemToCompanyArray, changeCompanyArrayItem, removeItemFromCompanyArray } from 'models/Company/CompanyProfile';
import RegistrationStatuses from 'models/Company/RegistrationStatuses';
import LegalNatures from 'models/Company/LegalNatures';
import { createAccount, deleteAccount } from 'api/company-requests/company-account-requests';
import { AuthContext } from 'contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { generateGuid } from 'utilities/Generator';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs, { Dayjs } from 'dayjs';
import { availableFinancialOptions } from 'models/Company/FinancialPosition';
import { availableEmployeeQuantity } from 'models/Company/EmployeeQuantities';
import { createCompanyProfile } from 'api/company-requests/company-profile-requests';

const CompanyForm: FC = () => {

  const [companyAccount, setCompanyAccount] = useState<CompanyAccount>({
    registrationStatus: "1",
    legalNature: "EI"
  } as CompanyAccount);

  const [companyProfile, setCompanyProfile] = useState<CompanyProfile>({
    financialCapital: 0,
    employees: 0,
    socialMedia: [{ title: '', url: '', username: '', key: generateGuid() }],
    addresses: [{ address: '', title: '', key: generateGuid() }]
  } as CompanyProfile)

  const { adminToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const [errorCreatingAccount, setErrorCreatingAccount] = useState<string>("");

  const [cnpj, setCnpj] = useState<string>("");

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

  const handlePasswordChange = debounce((element: HTMLInputElement) => {
    setCompanyAccount({ ...companyAccount, password: element.value });
  }, 350);

  const handleContactChange = debounce((element: HTMLInputElement) => {
    setCompanyProfile({ ...companyProfile, contact: element.value });
  }, 350);

  const handleWebisteChange = debounce((element: HTMLInputElement) => {
    setCompanyProfile({ ...companyProfile, url: element.value });
  }, 350);

  async function handleFormSubmit(e: any): Promise<void> {
    e.preventDefault();

    let response;
    let id: number;
    try {
      let accountToSend = { ...companyAccount, cnpj: cnpj };
      response = await createAccount(accountToSend, adminToken!);

      if (response.status === 201) {
        try {
          id = response.data.content.id;
          let profileToSend: CompanyProfile = {
            ...companyProfile,
            id: id
          };
          response = await createCompanyProfile(profileToSend, adminToken!);

          if (response.status === 201)
            navigate("/");
        } catch (error: any) {
          deleteAccount(id!, adminToken!);
          throw error;
        }
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

          <Grid container item sm={12} md={12} lg={12} display="flex">
            {companyProfile.addresses.map((x, index) => {
              const titleId: string = `title-address-${index}`;
              const addressId: string = `address-${index}`;
              const addressNumberId: string = `address-number-${index}`;

              return (
                <Fragment key={x.key}>
                  <Grid item sm={12} md={3} lg={4} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={titleId}
                      label="Title"
                      helperText="Describe what this address is"
                      fullWidth
                      value={x.title}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.addresses, index, "title",
                        e.target.value))}
                    />
                  </Grid>
                  <Grid item sm={12} md={3} lg={4} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={addressId}
                      label="Address"
                      helperText="Type the address"
                      fullWidth
                      value={x.address}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.addresses, index, "address",
                        e.target.value))}
                    />
                  </Grid>
                  <Grid item sm={12} md={3} lg={3} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={addressNumberId}
                      label="Number"
                      helperText="Insert the number of this address"
                      fullWidth
                      value={x.number}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.addresses, index, "number",
                        e.target.value))}
                    />
                  </Grid>
                </Fragment>
              )
            })}
          </Grid>

          <Grid container item display="flex" justifyContent="flex-end">
            <Button variant="contained" onClick={() => setCompanyProfile(addItemToCompanyArray(companyProfile, companyProfile.addresses))} style={{ marginRight: "1%" }}>Add Address</Button>
            <Button variant="outlined" onClick={() => setCompanyProfile(removeItemFromCompanyArray(companyProfile, companyProfile.addresses))}>Remove Address</Button>
          </Grid>

          <Grid item sm={12} md={6} lg={6}>
            <TextField
              id="contact"
              label="Contact"
              fullWidth
              onChange={(e) => handleContactChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid item lg={6} md={6} sm={12}>
            <DatePicker
              label="Select foundation date"
              maxDate={dayjs(new Date().toDateString())}
              slotProps={{
                textField: {
                  fullWidth: true
                }
              }}
              onChange={(val: Dayjs | null) => setCompanyProfile({ ...companyProfile, creationDate: val! })} />
          </Grid>

          <Grid item lg={6} md={6} sm={12}>
            <FormControl>
              <FormLabel id="capital-group-label">Financial capital</FormLabel>
              <RadioGroup
                aria-labelledby="capital-radio-group"
                name="capital-radio-buttons-group"
                value={companyProfile.financialCapital}
                onChange={(e) => setCompanyProfile({ ...companyProfile, financialCapital: Number.parseInt(e.target.value) as 0 | 1 | 2 | 3 })}
              >
                {availableFinancialOptions.map(x => (
                  <FormControlLabel key={x.key} value={x.key} control={<Radio />} label={x.description} />
                ))}
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item lg={6} md={6} sm={12}>
            <FormControl>
              <FormLabel id="employee-group-label">Employee quantity</FormLabel>
              <RadioGroup
                aria-labelledby="employee-radio-group"
                name="employee-radio-buttons-group"
                value={companyProfile.employees}
                onChange={(e) => setCompanyProfile({ ...companyProfile, employees: Number.parseInt(e.target.value) as 0 | 1 | 2 })}
              >
                {availableEmployeeQuantity.map(x => (
                  <FormControlLabel key={x.key} value={x.key} control={<Radio />} label={x.description} />
                ))}
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item sm={12} md={12} lg={12}>
            <TextField
              id="website"
              label="Website"
              fullWidth
              onChange={(e) => handleWebisteChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid container item sm={12} md={12} lg={12} display="flex">
            {companyProfile.socialMedia.map((x, index) => {
              const titleId: string = `title-social-media-${index}`;
              const urlId: string = `url-social-media-${index}`;
              const usernameId: string = `username-social-media-${index}`;
              return (
                <Fragment key={x.key}>
                  <Grid item sm={12} md={3} lg={4} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={titleId}
                      label="Title"
                      helperText="Type which is the social media"
                      fullWidth
                      value={x.title}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.socialMedia, index, "title",
                        e.target.value))}
                    />
                  </Grid>
                  <Grid item sm={12} md={3} lg={4} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={urlId}
                      label="Url"
                      helperText="Type the URL"
                      fullWidth
                      value={x.url}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.socialMedia, index, "url",
                        e.target.value))}
                    />
                  </Grid>
                  <Grid item sm={12} md={3} lg={3} style={{ marginRight: '2%', marginBottom: '1%' }}>
                    <TextField
                      id={usernameId}
                      label="Username"
                      helperText="Your username in this social media"
                      fullWidth
                      value={x.username}
                      onChange={(e) => setCompanyProfile(changeCompanyArrayItem(companyProfile, companyProfile.socialMedia, index, "username",
                        e.target.value))}
                    />
                  </Grid>
                </Fragment>
              )
            })}
          </Grid>

          <Grid container item display="flex" justifyContent="flex-end">
            <Button
              variant="contained"
              onClick={() => setCompanyProfile(addItemToCompanyArray(companyProfile, companyProfile.socialMedia))}
              style={{ marginRight: "1%" }}
            >
              Add Social Media
            </Button>
            <Button variant="outlined" onClick={() => setCompanyProfile(removeItemFromCompanyArray(companyProfile, companyProfile.socialMedia))}>Remove Social Media</Button>
          </Grid>

          <Grid item sm={12} md={12} lg={12}>
            <TextField
              required
              id="password"
              label="Password"
              fullWidth
              type="password"
              onChange={(e) => handlePasswordChange(e.target as HTMLInputElement)}
            />
          </Grid>

          <Grid container item justifyContent="flex-end" style={{ marginTop: '5%' }}>
            <Grid item>
              <Button variant="contained" type="submit">Create account</Button>
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </>
  )
}

export default CompanyForm;