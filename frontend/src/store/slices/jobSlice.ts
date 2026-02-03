import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  skills: string[];
  experience_level: string;
  salary?: string;
  source: string;
  url?: string;
  posted_date?: string;
  similarity_score?: number;
  skills_match?: number;
  experience_match?: number;
  overall_score?: number;
}

interface ResumeData {
  skills: string[];
  experience: string[];
  education: string[];
  full_name: string;
  email: string;
  phone?: string;
  location?: string;
}

interface JobState {
  jobs: Job[];
  resumeData: ResumeData | null;
  recommendations: Job[];
  isLoading: boolean;
  error: string | null;
  jobCount: number;
}

const initialState: JobState = {
  jobs: [],
  resumeData: null,
  recommendations: [],
  isLoading: false,
  error: null,
  jobCount: 0,
};

// Async thunks
export const parseResumeFile = createAsyncThunk(
  'jobs/parseResumeFile',
  async (file: File, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post('/api/parse-resume-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to parse resume');
    }
  }
);

export const parseResumeText = createAsyncThunk(
  'jobs/parseResumeText',
  async (resumeText: string, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/parse-resume-text', {
        resume_text: resumeText,
        top_k: 10,
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to parse resume');
    }
  }
);

export const getJobCount = createAsyncThunk(
  'jobs/getJobCount',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/job-count');
      return response.data.job_count;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to get job count');
    }
  }
);

export const ingestJobs = createAsyncThunk(
  'jobs/ingestJobs',
  async (jobs: Job[], { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/ingest-jobs', { jobs });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to ingest jobs');
    }
  }
);

const jobSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearRecommendations: (state) => {
      state.recommendations = [];
    },
    setResumeData: (state, action) => {
      state.resumeData = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Parse Resume File
      .addCase(parseResumeFile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(parseResumeFile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.resumeData = action.payload.resume_data;
        state.recommendations = action.payload.recommendations;
      })
      .addCase(parseResumeFile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Parse Resume Text
      .addCase(parseResumeText.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(parseResumeText.fulfilled, (state, action) => {
        state.isLoading = false;
        state.resumeData = action.payload.resume_data;
        state.recommendations = action.payload.recommendations;
      })
      .addCase(parseResumeText.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get Job Count
      .addCase(getJobCount.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getJobCount.fulfilled, (state, action) => {
        state.isLoading = false;
        state.jobCount = action.payload;
      })
      .addCase(getJobCount.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Ingest Jobs
      .addCase(ingestJobs.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(ingestJobs.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(ingestJobs.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearRecommendations, setResumeData } = jobSlice.actions;
export default jobSlice.reducer;