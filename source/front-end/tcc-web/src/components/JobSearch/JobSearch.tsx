import { InputAdornment, TextField } from '@mui/material';
import { Job } from 'models/Job/Job';
import SearchIcon from '@mui/icons-material/Search';

type Props = {
  allJobs: Job[];
  jobs: Job[];
  onSearchChange: (jobs: Job[]) => void;
}

const JobSearch = ({ allJobs, jobs, onSearchChange }: Props) => {

  function handleSearchChange(text: string): void {
    if (text === "") {
      onSearchChange(allJobs);
      return;
    }

    const jobsCopy: Job[] = jobs.filter(x => x.role!.includes(text));
    onSearchChange(jobsCopy);
  }

  return (
    <TextField
      id="search-box"
      label="Search for a job"
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon />
          </InputAdornment>
        ),
      }}
      onChange={(e) => handleSearchChange(e.target.value)}
      fullWidth
    />
  )
}

export default JobSearch