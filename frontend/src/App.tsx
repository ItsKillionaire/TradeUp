import React from 'react';
import Dashboard from './Dashboard';
import { Container, CssBaseline, ThemeProvider } from '@mui/material';
import theme from './Theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Dashboard />
      </Container>
    </ThemeProvider>
  );
}

export default App;