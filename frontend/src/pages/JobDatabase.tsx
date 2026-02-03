import React from 'react';
import { Box, Container, Typography, Card, CardContent, TextField, Button, Alert } from '@mui/material';
import { Dataset as DatabaseIcon } from '@mui/icons-material';

const JobDatabase: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Job Database
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Browse and search through our comprehensive job database to find opportunities that match your interests.
        </Typography>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6">Search Jobs</Typography>
            <DatabaseIcon color="primary" />
          </Box>
          <Box display="flex" gap={2} flexWrap="wrap">
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search by title, company, or keywords..."
              sx={{ mb: 2 }}
            />
            <Button variant="contained" color="primary">
              Search
            </Button>
            <Button variant="outlined" color="primary">
              Clear Filters
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Alert severity="info" sx={{ mb: 3 }}>
        No jobs found in the database. Please ingest some job data first to see results.
      </Alert>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6">About the Job Database</Typography>
            <DatabaseIcon color="primary" />
          </Box>
          <Typography variant="body2" color="text.secondary" paragraph>
            Our job database contains listings from various sources including:
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • Job boards and career websites
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • Company career pages
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • RSS feeds and APIs
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Jobs are regularly updated and processed through our AI system for better matching.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default JobDatabase;