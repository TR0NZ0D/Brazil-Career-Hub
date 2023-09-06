import {
  Button,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField,
  Typography
} from '@mui/material';
import { JobCreationContainer, Logo } from './styles';
import LogoImage from 'assets/images/logo.png';
import { useContext, useState } from 'react';
import { createJob } from 'api/job/job-requests';
import { Job } from 'models/Job/Job';
import { AuthContext } from 'contexts/AuthContext';
import { CompanyAuth } from 'models/Company/CompanyAuth';
import { useNavigate } from 'react-router-dom';

const CreateJob = () => {

  const { adminToken, entityLogged } = useContext(AuthContext);

  const [role, setRole] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [modality, setModality] = useState<"remote" | "onsite">("remote");
  const [salary, setSalary] = useState<number | undefined>();

  const [addressTitle, setAddressTitle] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [addressNumber, setAddressNumber] = useState<number>(100);

  const navigate = useNavigate();

  async function handleCreateJobSubmit(e: any) {
    e.preventDefault();

    try {
      const entity = entityLogged as CompanyAuth;
      let jobData: Job = {
        role,
        description,
        modality,
        salary,
        address: null,
        companyId: entity.company_account
      }

      if (modality === "onsite") {
        jobData.address = {
          address: address,
          title: addressTitle,
          number: addressNumber
        }
      }
      await createJob(jobData, adminToken!);
      navigate("/");
    } catch (error) {
      console.log(error);
      alert("An error happened while creating this job");
    }
  }

  return (
    <Grid container display="flex" alignItems="center" justifyContent="center" flexDirection="column">
      <Logo src={LogoImage} alt="logo" />

      <JobCreationContainer onSubmit={handleCreateJobSubmit}>
        <Typography variant="h5">Create Job</Typography>

        <Grid container display="flex" spacing={2} style={{ marginTop: "3%" }}>
          <Grid container item display="flex" spacing={2} lg={12} justifyContent="space-around">
            <Grid item lg={6}>
              <TextField
                id="role"
                label="Role"
                required
                variant="outlined"
                fullWidth
                value={role}
                onChange={(e) => setRole(e.target.value)}
              />
            </Grid>

            <Grid item lg={6}>
              <FormControl>
                <FormLabel id="row-modality-group-label">Modality</FormLabel>
                <RadioGroup
                  row
                  aria-labelledby="row-modality-group-label"
                  name="row-modality-buttons-group"
                  value={modality}
                  onChange={(e) => setModality(e.target.value as "remote" | "onsite")}
                >
                  <FormControlLabel value="remote" control={<Radio />} label="Remote" />
                  <FormControlLabel value="onsite" control={<Radio />} label="On office" />
                </RadioGroup>
              </FormControl>
            </Grid>
          </Grid>

          <Grid item lg={12}>
            <TextField
              id="description"
              label="Description"
              required
              variant="outlined"
              fullWidth
              multiline
              rows={13}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Grid>

          <Grid item lg={12}>
            <TextField
              id="annual-salary"
              label="Annual Salary"
              variant="outlined"
              fullWidth
              type="number"
              value={salary}
              onChange={(e) => setSalary(Number.parseFloat(e.target.value))}
            />
          </Grid>

          {modality === "onsite" &&
            <>
              <Grid item lg={4}>
                <TextField
                  id="address-title"
                  label="Title"
                  variant="outlined"
                  fullWidth
                  value={addressTitle}
                  onChange={(e) => setAddressTitle(e.target.value)}
                />
              </Grid>

              <Grid item lg={4}>
                <TextField
                  id="address"
                  label="Address"
                  variant="outlined"
                  fullWidth
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                />
              </Grid>

              <Grid item lg={4}>
                <TextField
                  id="address-number"
                  label="Number"
                  variant="outlined"
                  fullWidth
                  value={addressNumber}
                  onChange={(e) => setAddressNumber(Number.parseInt(e.target.value))}
                />
              </Grid>
            </>}

        </Grid>

        <Grid container item lg={12} display="flex" justifyContent="flex-end" style={{ marginTop: "5%" }}>
          <Button type="submit" variant="contained">Submit</Button>
        </Grid>
      </JobCreationContainer>
    </Grid>
  )
}

export default CreateJob;