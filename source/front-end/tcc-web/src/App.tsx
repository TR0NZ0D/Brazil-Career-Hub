import Navbar from './components/Navbar/Navbar';
import { ThemeProvider } from 'styled-components';
import { theme } from './styles/theme';
import { AuthContextProvider } from 'contexts/AuthContext';
import { RouterProvider } from 'react-router-dom';
import router from './router';

function App() {
  return (
    <AuthContextProvider>
      <ThemeProvider theme={theme}>
        <Navbar />
        <RouterProvider router={router} />
      </ThemeProvider>
    </AuthContextProvider>
  );
}

export default App;
