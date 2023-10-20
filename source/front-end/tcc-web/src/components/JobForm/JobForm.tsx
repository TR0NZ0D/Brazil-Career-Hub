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
import { JobCreationContainer } from './styles';
import { useContext, useEffect, useState } from 'react';
import { createJob, deleteJob, updateJob } from 'api/job/job-requests';
import { Job } from 'models/Job/Job';
import { AuthContext } from 'contexts/AuthContext';
import { CompanyAuth } from 'models/Company/CompanyAuth';

type Props = {
  job?: Job;
  onActionExecuted?: () => void;
}

const JobForm = ({ job, onActionExecuted }: Props) => {

  const { adminToken, entityLogged } = useContext(AuthContext);

  const [formAction, setFormAction] = useState<"create" | "update">("create");
  const [role, setRole] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [modality, setModality] = useState<"remote" | "onsite">("remote");
  const [salary, setSalary] = useState<number>(1320);

  const [addressTitle, setAddressTitle] = useState<string>("");
  const [address, setAddress] = useState<string>("");
  const [addressNumber, setAddressNumber] = useState<number>(100);

  useEffect(() => {
    if (job !== undefined) {
      mapJobProp();
      setFormAction("update");
    }

    else {
      resetProps();
    }
  }, [job]);

  function resetProps(): void {
    setRole("");
    setDescription("");
    setModality("remote");
    setSalary(1320);
    setAddressTitle("");
    setAddress("");
    setAddressNumber(100);
  }

  function mapJobProp(): void {
    setRole(job!.role);
    setDescription(job!.description);
    setModality(job!.modality);
    setSalary(job!.salary!);

    if (job?.address) {
      setAddressTitle(job!.address.title);
      setAddress(job!.address.address);
      setAddressNumber(job!.address.number!);
    }
  }

  function handleCreateJobSubmit() {
    const jobData: Job = buildJob();
    createJob(jobData, adminToken!)
      .then(response => {
        if (response.status === 201) {
          if (onActionExecuted) {
            onActionExecuted();
          }
        }
      })
      .catch(() => {
        alert("An error happened while creating this job");
      })
  }

  function handleUpdateJobClick(): void {
    let updatedJob = buildJob();
    updatedJob.pk = job?.pk;
    updateJob(updatedJob, adminToken!)
      .then(response => {
        if (response.status === 200) {
          if (onActionExecuted)
            onActionExecuted();
        }
      })
      .catch(() => {
        alert("An error happened while updating this job");
      })
  }

  function handleJobDeleteClick(): void {
    deleteJob(job!.pk!, adminToken!)
      .then(response => {
        if (response.status === 204) {
          if (onActionExecuted) {
            onActionExecuted();
          }
        }
      })
      .catch(() => {
        alert("Could not delete this job!");
      })
  }

  function buildJob(): Job {
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

    return jobData;
  }

  return (
    <JobCreationContainer>

      {formAction === "create" &&
        <Typography variant="h5">Create Job</Typography>}

      {formAction === "update" &&
        <Typography variant="h5">Review Job</Typography>}

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

      <Grid
        container
        item lg={12}
        display="flex"
        justifyContent="flex-end"
        gap={2}
        style={{ marginTop: "5%" }}
      >
        {formAction === "update" &&
          <>
            <Button
              onClick={handleJobDeleteClick}
              variant="contained"
            >
              Delete
            </Button>

            <Button
              onClick={handleUpdateJobClick}
              variant="contained"
            >
              Update
            </Button>
          </>}

        {formAction === "create" &&
          <Button
            onClick={handleCreateJobSubmit}
            variant="contained"
          >
            Submit
          </Button>}
      </Grid>
    </JobCreationContainer>
  )
}

export default JobForm;