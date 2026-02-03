import React, { useState } from 'react';
import { Box, Container, Typography, Card, CardContent, Button, Alert } from '@mui/material';
import { Upload as UploadIcon } from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';

const ResumeUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    setError(null);
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      // Check file type
      if (!file.type.includes('pdf') && !file.type.includes('msword') && !file.type.includes('openxmlformats-officedocument')) {
        setError('Please upload a PDF or Word document');
        return;
      }
      setFile(file);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      // TODO: Implement actual upload logic
      console.log('Uploading file:', file);
      // const response = await uploadResume(file);
      // Handle response
    } catch (err) {
      setError('Failed to upload resume. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Resume Upload
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload your resume to get personalized job recommendations. We support PDF and Word documents.
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
              transition: 'all 0.3s ease'
            }}
          >
            <input {...getInputProps()} />
            <UploadIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume here'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              or click to select a file
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
              Supported formats: PDF, DOC, DOCX
            </Typography>
          </Box>

          {file && (
            <Box sx={{ mt: 3, p: 2, backgroundColor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Selected file: {file.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Size: {(file.size / 1024).toFixed(2)} KB
              </Typography>
            </Box>
          )}

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              onClick={() => setFile(null)}
              disabled={!file}
            >
              Clear
            </Button>
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!file || uploading}
              startIcon={<UploadIcon />}
            >
              {uploading ? 'Uploading...' : 'Upload Resume'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Box sx={{ mt: 4 }}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Tips for Best Results
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              • Use a clear, well-formatted resume
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              • Include your skills, experience, and education
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              • PDF format is recommended for best parsing accuracy
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default ResumeUpload;