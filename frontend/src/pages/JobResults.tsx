import React from 'react';
import { Box, Container, Typography, Card, CardContent, Alert } from '@mui/material';
import { Work as WorkIcon } from '@mui/icons-material';

const JobResults: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Job Recommendations
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Based on your resume analysis, here are the top job matches for you.
        </Typography>
      </Box>

      <Alert severity="info" sx={{ mb: 3 }}>
        No resume uploaded yet. Please upload your resume first to see job recommendations.
      </Alert>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6">How it works</Typography>
            <WorkIcon color="primary" />
          </Box>
          <Typography variant="body2" color="text.secondary" paragraph>
            Our AI analyzes your resume and matches it against available job postings using:
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • Semantic similarity analysis
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • Skills matching
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            • Experience level alignment
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Upload your resume to get started!
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default JobResults;