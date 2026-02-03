import React, { useState } from 'react';
import { Box, Container, Paper, TextField, Button, Typography, Alert, Link, Grid } from '@mui/material';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { loginUser, registerUser } from '../store/slices/authSlice';
import { useNavigate } from 'react-router-dom';

const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
  });
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { isLoading, error } = useAppSelector((state) => state.auth);

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }
    
    if (!isLogin) {
      if (!formData.email.trim()) {
        newErrors.email = 'Email is required';
      } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
        newErrors.email = 'Email is invalid';
      }
      
      if (!formData.full_name.trim()) {
        newErrors.full_name = 'Full name is required';
      }
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      if (isLogin) {
        await dispatch(loginUser({
          username: formData.username,
          password: formData.password,
        })).unwrap();
        navigate('/');
      } else {
        await dispatch(registerUser({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
        })).unwrap();
        navigate('/');
      }
    } catch (err: any) {
      // Error is handled by the slice
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={6}
          sx={{
            p: 4,
            borderRadius: 3,
            boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
          }}
        >
          <Typography variant="h4" component="h1" align="center" gutterBottom>
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </Typography>
          <Typography variant="body2" color="text.secondary" align="center" gutterBottom>
            {isLogin 
              ? 'Sign in to access your job recommendations' 
              : 'Join us to get personalized job matches'
            }
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              {!isLogin && (
                <>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Full Name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      error={!!errors.full_name}
                      helperText={errors.full_name}
                      required
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      error={!!errors.email}
                      helperText={errors.email}
                      required={!isLogin}
                    />
                  </Grid>
                </>
              )}
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  error={!!errors.username}
                  helperText={errors.username}
                  required
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  error={!!errors.password}
                  helperText={errors.password}
                  required
                />
              </Grid>
            </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              sx={{ mt: 3, mb: 2, py: 1.5 }}
            >
              {isLoading ? 'Loading...' : isLogin ? 'Sign In' : 'Sign Up'}
            </Button>
          </form>

          <Box textAlign="center">
            <Link
              component="button"
              variant="body2"
              onClick={() => {
                setIsLogin(!isLogin);
                setErrors({});
                setFormData({
                  username: '',
                  email: '',
                  password: '',
                  full_name: '',
                });
              }}
              sx={{ cursor: 'pointer' }}
            >
              {isLogin 
                ? "Don't have an account? Sign Up" 
                : "Already have an account? Sign In"
              }
            </Link>
          </Box>

          <Box mt={3} textAlign="center">
            <Typography variant="body2" color="text.secondary">
              Demo credentials: admin / admin123
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default AuthPage;