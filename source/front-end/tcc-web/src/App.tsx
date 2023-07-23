import Navbar from './components/Navbar/Navbar';
import { ThemeProvider } from 'styled-components';
import { theme } from './styles/theme';
import { AuthContextProvider } from 'contexts/AuthContext';
import { RouterProvider } from 'react-router-dom';
import router from './router';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

function App() {
  return (
    <AuthContextProvider>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <ThemeProvider theme={theme}>
          <Navbar />
          <RouterProvider router={router} />
        </ThemeProvider>
      </LocalizationProvider>
    </AuthContextProvider>
  );
}

export default App;
