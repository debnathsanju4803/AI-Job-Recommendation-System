import React from 'react';
import { AppBar, Toolbar, Typography, Container, Box, IconButton, Drawer, List, ListItem, ListItemIcon, ListItemText, useTheme, useMediaQuery } from '@mui/material';
import { Menu as MenuIcon, DarkMode as DarkModeIcon, LightMode as LightModeIcon, Dashboard as DashboardIcon, Upload as UploadIcon, Work as WorkIcon, Dataset as DatabaseIcon, Logout as LogoutIcon } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { toggleDarkMode, toggleSidebar } from '../store/slices/uiSlice';
import { logoutUser } from '../store/slices/authSlice';
import { useNavigate } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
  darkMode: boolean;
  setDarkMode: (darkMode: boolean) => void;
}

const Layout: React.FC<LayoutProps> = ({ children, darkMode, setDarkMode }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { sidebarOpen } = useAppSelector((state) => state.ui);
  const { user } = useAppSelector((state) => state.auth);

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Resume Upload', icon: <UploadIcon />, path: '/resume' },
    { text: 'Job Results', icon: <WorkIcon />, path: '/results' },
    { text: 'Job Database', icon: <DatabaseIcon />, path: '/jobs' },
  ];

  const handleLogout = () => {
    dispatch(logoutUser());
    navigate('/auth');
  };

  const toggleTheme = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    dispatch(toggleDarkMode());
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={() => dispatch(toggleSidebar())}
            sx={{ mr: 2, ...(isMobile && { display: 'block' }) }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI Job Recommendation System
          </Typography>

          <IconButton color="inherit" onClick={toggleTheme} sx={{ mr: 1 }}>
            {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>

          {user && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="body2">
                Welcome, {user.full_name}
              </Typography>
              <IconButton color="inherit" onClick={handleLogout}>
                <LogoutIcon />
              </IconButton>
            </Box>
          )}
        </Toolbar>
      </AppBar>

      <Drawer
        variant={isMobile ? "temporary" : "permanent"}
        open={isMobile ? sidebarOpen : true}
        onClose={() => dispatch(toggleSidebar())}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
            top: ['56px', '64px'],
            height: 'calc(100% - 56px)',
            [theme.breakpoints.up('sm')]: {
              height: 'calc(100% - 64px)',
            },
          },
        }}
      >
        <List>
          {menuItems.map((item) => (
            <ListItem 
              button 
              key={item.text}
              onClick={() => navigate(item.path)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: theme.palette.action.selected,
                },
              }}
            >
              <ListItemIcon>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItem>
          ))}
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: ['56px', '64px'],
          width: { sm: `calc(100% - 240px)` },
        }}
      >
        <Container maxWidth="xl">
          {children}
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;