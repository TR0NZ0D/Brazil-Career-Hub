import Navbar from './components/Navbar/Navbar';
import { ThemeProvider } from 'styled-components';
import { theme } from './styles/theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <Navbar />
      </div>
    </ThemeProvider>
  );
}

export default App;
