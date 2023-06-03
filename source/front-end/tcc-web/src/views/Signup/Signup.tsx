import { FC, useState } from 'react';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';

const Signup: FC = () => {

  const [tabValue, setTabValue] = useState(0);

  return (
    <Grid container style={{ height: "100%" }}>
      <Grid item xs={2} md={2} sm={0}>
      </Grid>

      <Grid item xs={8} md={8} sm={12}>
        <Container style={{
          borderRadius: "10",
          margin: "7% 0 5% 0",
          border: "2px solid #ebe8e8",
          boxShadow: "0px 4px 4px rgba(0, 0, 0, 0.25)",
          padding: "2%"
        }}>
          <Tabs value={tabValue} onChange={(_, index) => setTabValue(index)} aria-label="options-tab">
            <Tab label="I wanna be hired!" />
            <Tab label="I wanna hire!" />
          </Tabs>

          <Container style={{ padding: "4% 2% 2% 2%" }}>
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

            <Grid container spacing={2} component="form">
              {tabValue === 0 &&
                <>
                  <Grid item>
                    <TextField
                      required
                      id="username"
                      label="Username"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="name"
                      label="Name"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="surname"
                      label="Surname"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="age"
                      label="Age"
                      type="number"
                    />
                  </Grid>

                  <Grid item>
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

                  {/* Todo: Add CPF mask */}
                  <Grid item>
                    <TextField
                      required
                      id="CPF"
                      label="CPF"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="job-id"
                      label="Number of your job registration"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="email"
                      label="E-mail"
                      type="email"
                    />
                  </Grid>

                  {/* Todo: Add nationality */}

                  <Grid item>
                    <TextField
                      required
                      id="address"
                      label="Address"
                    />
                  </Grid>

                  {/* Todo: Add languages */}

                  <Grid item>
                    <TextField
                      required
                      id="portfolio"
                      label="Website for your portfolio"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="social-media"
                      label="Social media"
                    />
                  </Grid>

                  <Grid item>
                    <TextField
                      required
                      id="cellphone"
                      label="Contact phone"
                    />
                  </Grid>
                </>
              }

              {tabValue === 1 &&
                <TextField
                  required
                  id="CNPJ"
                />}

              <Grid container item justifyContent="flex-end">
                <Grid item>
                  <Button>Submit</Button>
                </Grid>
              </Grid>
            </Grid>
          </Container>
        </Container>
      </Grid>

      <Grid item xs={2} md={2} sm={0}>
      </Grid>
    </Grid>
  )
};

export default Signup;