import {useMemo} from 'react'
import {createTheme} from '@mui/material/styles'

export const themeSettings = (mode) => {
    return {
        palette: {
            primary: {
                main: '#fff',
                contrastText: '#000'
            },
            neutral: {
                main: '#fff',
                contrastText: '#000'
            }
        },
        components: {
            MuiButton: {
                styleOverrides: {
                    root: {
                        color: '#004b87',
                        '&:hover': {
                            color: '#d14124'
                        }
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
                        cursor: 'pointer'
                    }
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
