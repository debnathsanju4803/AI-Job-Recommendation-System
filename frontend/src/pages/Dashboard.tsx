import React from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, Chip } from '@mui/material';
import { Dashboard as DashboardIcon, Upload as UploadIcon, Work as WorkIcon, Dataset as DatabaseIcon } from '@mui/icons-material';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome to your AI Job Recommendation System. Get started by uploading your resume or exploring job opportunities.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Resume Upload</Typography>
                <UploadIcon color="primary" />
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                Upload your resume to get personalized job recommendations based on your skills and experience.
              </Typography>
              <Chip label="Start Here" color="primary" variant="outlined" />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Job Results</Typography>
                <WorkIcon color="primary" />
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                View your personalized job recommendations with detailed scoring and matching analysis.
              </Typography>
              <Chip label="View Results" color="secondary" variant="outlined" />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">Job Database</Typography>
                <DatabaseIcon color="primary" />
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                Browse and search through our comprehensive job database to find opportunities.
              </Typography>
              <Chip label="Browse Jobs" color="info" variant="outlined" />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">System Status</Typography>
                <DashboardIcon color="primary" />
              </Box>
              <Typography variant="body2" color="text.secondary" paragraph>
                Check system status, job count, and other important metrics.
              </Typography>
              <Chip label="System Info" color="success" variant="outlined" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box mt={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Quick Stats
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body2" color="text.secondary">Jobs in Database</Typography>
                <Typography variant="h6">0</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body2" color="text.secondary">Resumes Processed</Typography>
                <Typography variant="h6">0</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body2" color="text.secondary">Active Users</Typography>
                <Typography variant="h6">1</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body2" color="text.secondary">System Status</Typography>
                <Typography variant="h6" color="success.main">Online</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Dashboard;