import React from 'react';
import Dashboard from './Dashboard';
import { Container, CssBaseline } from '@mui/material';

function App() {
  return (
    <div className="App">
      <CssBaseline />
      <Container>
        <Dashboard />
      </Container>
    </div>
  );
}

export default App;