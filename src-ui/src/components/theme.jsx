import {useMemo} from 'react'
import {createTheme} from '@mui/material/styles'

export const themeSettings = (mode) => {
    return {
        palette: {
            primary: {
                main: '#004b87',
            },
            secondary: {
                main: '#fff',
            },
            text: {
                primary: '#000',
                secondary: '#004b87',
            },
            //divider: '#d14124',
        },
        components: {
            MuiTypography: {
                styleOverrides: {
                    root: {
                        fontFamily: '"Open Sans", "Roboto", "Helvetica", "Arial", sans-serif',
                        cursor: 'default',
                    }
                }
            },
            MuiOutlinedInput: {
                styleOverrides: {
                    root: {
                        '& .MuiOutlinedInput-notchedOutline': {
                            borderColor: '#004b87',
                        },

                    }
                }
            },
            MuiTextField: {
                styleOverrides: {
                    root: {}
                }
            },
            MuiButton: {
                styleOverrides: {
                    secondary: {
                        color: '#004b87',
                        '&:hover': {
                            color: '#d14124'
                        },
                        textTransform: 'none'
                    }
                }
            },
            MuiTab: {
                styleOverrides: {
                    root: {
                        color: '#004b87',
                        '&:hover': {
                            color: '#d14124'
                        },
                        '&.Mui-selected': {
                            color: '#d14124', // Your desired color for the selected tab
                        },
                    }
                }
            },
            MuiLink: {
                styleOverrides: {
                    root: {
                        color: '#004b87',
                        '&:hover': {
                            color: '#d14124'
                        },
                        cursor: 'pointer',
                        textDecoration: 'none',
                    }
                }
            },
            ListItemIcon: {
                styleOverrides: {
                    root: {}
                }
            }
        }
    };
}

export const useTheme = () => {
    // Implement store for mode setting
    const mode = 'light';
    return useMemo(() => createTheme(themeSettings(mode)), [mode]);
}

export default useTheme
