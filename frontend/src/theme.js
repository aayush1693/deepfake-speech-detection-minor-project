import { createMuiTheme } from '@material-ui/core/styles';
import { responsiveFontSizes } from '@material-ui/core';

// Constants for commonly used values
const COMMON_CONSTANTS = {
  FONT_FAMILY: 'Roboto, Arial, sans-serif',
  TRANSITION_BASE: 'all 0.3s ease-in-out',
  BORDER_RADIUS: 12,
  SPACING_UNIT: 8,
};

// Common typography settings
const commonTypography = {
  fontFamily: COMMON_CONSTANTS.FONT_FAMILY,
  h1: { fontSize: '2.5rem', fontWeight: 700 },
  h2: { fontSize: '2rem', fontWeight: 600 },
  h3: { fontSize: '1.75rem', fontWeight: 500 },
  body1: { fontSize: '1rem', lineHeight: 1.6 },
  button: { textTransform: 'uppercase' },
};

// Common breakpoints
const commonBreakpoints = {
  values: {
    xs: 0,
    sm: 600,
    md: 960,
    lg: 1280,
    xl: 1920,
  },
};

// Common transitions
const commonTransitions = {
  duration: {
    shortest: 150,
    shorter: 200,
    short: 250,
    standard: 300,
    complex: 375,
    enteringScreen: 225,
    leavingScreen: 195,
  },
  easing: {
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
  },
};

// Common component overrides
const commonOverrides = {
  MuiButton: {
    root: {
      borderRadius: COMMON_CONSTANTS.BORDER_RADIUS,
      textTransform: 'capitalize',
      padding: '12px 24px',
      fontSize: '1rem',
      transition: COMMON_CONSTANTS.TRANSITION_BASE,
    },
  },
  MuiPaper: {
    root: {
      padding: '16px',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      transition: 'box-shadow 0.3s ease-in-out',
      '&:hover': {
        boxShadow: '0 8px 12px rgba(0, 0, 0, 0.2)',
      },
    },
  },
  MuiContainer: {
    root: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
    },
  },
  MuiTypography: {
    root: {
      textAlign: 'center',
    },
  },
  MuiGrid: {
    container: {
      justifyContent: 'center',
      alignItems: 'center',
    },
  },
  MuiAppBar: {
    root: {
      backgroundColor: '#333',
      color: '#fff',
      padding: '10px 0',
    },
  },
  MuiDrawer: {
    paper: {
      width: 240,
      backgroundColor: '#f4f4f4',
    },
  },
  MuiListItem: {
    root: {
      '&$selected': {
        backgroundColor: '#e0e0e0',
        '&:hover': {
          backgroundColor: '#d5d5d5',
        },
      },
    },
  },
  MuiCard: {
    root: {
      borderRadius: COMMON_CONSTANTS.BORDER_RADIUS,
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      transition: COMMON_CONSTANTS.TRANSITION_BASE,
      '&:hover': {
        boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)',
      },
    },
  },
  MuiCardContent: {
    root: {
      padding: COMMON_CONSTANTS.SPACING_UNIT * 2,
    },
  },
  MuiCardActions: {
    root: {
      justifyContent: 'flex-end',
    },
  },
  MuiTable: {
    root: {
      minWidth: 650,
    },
  },
  MuiTableCell: {
    head: {
      backgroundColor: '#f5f5f5',
      fontWeight: 'bold',
    },
    body: {
      fontSize: 14,
    },
  },
  MuiTableRow: {
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: '#f9f9f9',
      },
    },
  },
  MuiTooltip: {
    tooltip: {
      backgroundColor: '#333',
      color: '#fff',
      fontSize: '0.875rem',
    },
  },
  MuiSnackbar: {
    root: {
      bottom: 70,
    },
  },
  MuiSnackbarContent: {
    root: {
      backgroundColor: '#333',
      color: '#fff',
    },
  },
  MuiAvatar: {
    root: {
      width: 40,
      height: 40,
    },
  },
  MuiChip: {
    root: {
      borderRadius: COMMON_CONSTANTS.BORDER_RADIUS,
      padding: '0 8px',
    },
  },
  MuiTabs: {
    root: {
      borderBottom: '1px solid #e0e0e0',
    },
  },
  MuiTab: {
    root: {
      textTransform: 'none',
      minWidth: 72,
      fontWeight: 500,
      marginRight: COMMON_CONSTANTS.SPACING_UNIT * 4,
      '&:hover': {
        color: '#40a9ff',
        opacity: 1,
      },
      '&$selected': {
        color: '#1890ff',
        fontWeight: 700,
      },
      '&:focus': {
        color: '#40a9ff',
      },
    },
  },
  MuiBadge: {
    root: {
      '& .MuiBadge-badge': {
        right: -3,
        top: 13,
        border: `2px solid ${COMMON_CONSTANTS.BORDER_RADIUS}`,
        padding: '0 4px',
      },
    },
  },
  MuiAccordion: {
    root: {
      border: '1px solid rgba(0, 0, 0, .125)',
      boxShadow: 'none',
      '&:not(:last-child)': {
        borderBottom: 0,
      },
      '&:before': {
        display: 'none',
      },
      '&$expanded': {
        margin: 'auto',
      },
    },
  },
  MuiAccordionSummary: {
    root: {
      backgroundColor: 'rgba(0, 0, 0, .03)',
      borderBottom: '1px solid rgba(0, 0, 0, .125)',
      marginBottom: -1,
      minHeight: 56,
      '&$expanded': {
        minHeight: 56,
      },
    },
    content: {
      '&$expanded': {
        margin: '12px 0',
      },
    },
  },
  MuiAccordionDetails: {
    root: {
      padding: COMMON_CONSTANTS.SPACING_UNIT * 2,
    },
  },
  MuiPagination: {
    ul: {
      justifyContent: 'center',
    },
  },
};

// Optimized shadow creation using memoization
const createShadows = (() => {
  const shadowCache = new Map();
  
  return (level) => {
    if (!shadowCache.has(level)) {
      shadowCache.set(level, Array(25).fill(level));
    }
    return shadowCache.get(level);
  };
})();

// Base theme creation function
const createBaseTheme = (isDark) => ({
  palette: {
    type: isDark ? 'dark' : 'light',
    primary: {
      main: '#000000',
    },
    secondary: {
      main: isDark ? '#90caf9' : '#3f51b5',
    },
    background: {
      default: isDark ? '#121212' : '#ffffff',
      paper: isDark ? '#1d1d1d' : '#f8f8f8',
    },
    text: {
      primary: isDark ? '#ffffff' : '#000000',
      secondary: isDark ? '#90caf9' : '#3f51b5',
    },
  },
  typography: commonTypography,
  shadows: createShadows('none'),
  spacing: COMMON_CONSTANTS.SPACING_UNIT,
  breakpoints: commonBreakpoints,
  transitions: commonTransitions,
  overrides: {
    ...commonOverrides,
    MuiButton: {
      ...commonOverrides.MuiButton,
      root: {
        ...commonOverrides.MuiButton.root,
        '&:hover': {
          backgroundColor: isDark ? '#ffffff' : '#000000',
          color: isDark ? '#000000' : '#ffffff',
        },
      },
    },
  },
});

// Create themes
const lightTheme = responsiveFontSizes(createMuiTheme(createBaseTheme(false)));
const darkTheme = responsiveFontSizes(createMuiTheme(createBaseTheme(true)));

export { lightTheme, darkTheme };
