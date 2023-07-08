import Navbar from './components/Navbar/Navbar';
import { ThemeProvider } from 'styled-components';
import { theme } from './styles/theme';
import { AuthContextProvider } from 'contexts/AuthContext';

function App() {
  return (
    <AuthContextProvider>
      <ThemeProvider theme={theme}>
        <Navbar />
      </ThemeProvider>
    </AuthContextProvider>
  );
}

export default App;
