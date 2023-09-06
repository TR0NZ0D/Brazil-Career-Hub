import { Button, Container, Grid, Typography } from '@mui/material';
import React, { useState } from 'react';
import WorkIcon from '@mui/icons-material/Work';
import { HomeContainer } from './styles';
import { useNavigate } from 'react-router-dom';

const CompanyHome = () => {

  const [vacancies, setVacancies] = useState([]);

  const navigate = useNavigate();

  return (
    <HomeContainer>

      {vacancies.length > 0 &&
        <div>Hello</div>}

      {vacancies.length === 0 &&
        <>
          <Grid
            container
            display="flex"
            justifyContent="center"
            alignItems="center"
            style={{ height: "30%" }}
          >
            <Grid
              container
              item
              lg={8}
              display="flex"
              flexDirection="column"
              justifyContent="center"
              alignItems="center"
            >
              <WorkIcon sx={{ fontSize: 80 }} style={{ fill: "#3E89FA" }} />
              <Typography variant="h6" gutterBottom>It looks like you haven't created a job</Typography>
              <Button variant="contained" onClick={() => navigate("/createJob")}>Create job</Button>
            </Grid>

            <Grid item lg={4}>
              <div>Hello world</div>
            </Grid>
          </Grid>
        </>}
    </HomeContainer>
  )
}

export default CompanyHome;