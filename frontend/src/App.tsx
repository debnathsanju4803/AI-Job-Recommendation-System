import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Provider } from 'react-redux';
import { store } from './store';
import { useAppSelector } from './store/hooks';

// Pages
import Dashboard from './pages/Dashboard';
import AuthPage from './pages/AuthPage';
import ResumeUpload from './pages/ResumeUpload';
import JobResults from './pages/JobResults';
import JobDatabase from './pages/JobDatabase';

// Layout
import Layout from './components/Layout';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = React.useState(false);
  
  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#2563eb',
      },
      secondary: {
        main: '#64748b',
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
  });

  const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated } = useAppSelector((state) => state.auth);
    return isAuthenticated ? <>{children}</> : <Navigate to="/auth" />;
  };

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout darkMode={darkMode} setDarkMode={setDarkMode}>
            <Routes>
              <Route path="/auth" element={<AuthPage />} />
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/resume" 
                element={
                  <ProtectedRoute>
                    <ResumeUpload />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/results" 
                element={
                  <ProtectedRoute>
                    <JobResults />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/jobs" 
                element={
                  <ProtectedRoute>
                    <JobDatabase />
                  </ProtectedRoute>
                } 
              />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </Provider>
  );
};

export default App;