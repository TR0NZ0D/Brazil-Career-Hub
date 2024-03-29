import { ThemeProvider } from 'styled-components';
import { theme } from './styles/theme';
import { AuthContextProvider } from 'contexts/AuthContext';
import { RouterProvider } from 'react-router-dom';
import router from './router';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { UIContextProvider } from 'contexts/UIContext';

function App() {
  return (
    <AuthContextProvider>
      <UIContextProvider>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <ThemeProvider theme={theme}>
            <RouterProvider router={router} />
          </ThemeProvider>
        </LocalizationProvider>
      </UIContextProvider>
    </AuthContextProvider>
  );
}

export default App;
