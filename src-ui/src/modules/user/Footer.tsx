import * as React from 'react';
import {useNavigate} from "react-router-dom";
import {Container, AppBar, Toolbar, Typography, Link} from '@mui/material';
import Box from "@mui/material/Box";
import Logo from "@app/assets/img/logo1-icon.svg";
import packageJSON from '../../../package.json';

function ResponsiveAppBar() {
    const navigate = useNavigate();

    const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        navigate(e.currentTarget.dataset.path!);
        return true;
    };

    return (
        <AppBar position="fixed" sx={{top: 'auto', bottom: 0, height: '30px'}}>
            <Container maxWidth={false} disableGutters sx={{pl: 1}}>
                <Toolbar disableGutters sx={{alignItems: 'flex-start', justifyContent: 'space-between'}}>
                    <Box sx={{display: 'flex', alignItems: 'center'}}>
                        <Link data-path="/" onClick={handleNavClick} sx={{mr: 1}} title="DNSMin Home">
                            <Typography
                                variant="body1"
                                noWrap
                                sx={{
                                    mt: 0.6,
                                    display: {xs: 'none', md: 'flex'},
                                    fontFamily: 'monospace',
                                    fontWeight: 700,
                                    letterSpacing: '.3rem',
                                    color: 'inherit',
                                    textDecoration: 'none',
                                }}
                            >
                                <Box sx={{display: {xs: 'none', md: 'flex'}, mr: 0.5}}>
                                    <img src={Logo} alt="DNSMin Logo" height={20}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>
                        <Typography
                            variant="body1"
                            noWrap
                            sx={{
                                mt: 0.8,
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'roboto',
                                fontWeight: 500,
                                fontSize: 14,
                                color: 'inherit',
                                textDecoration: 'none',
                            }}
                        >
                            Built for Big DNS
                        </Typography>
                    </Box>
                    <Box sx={{display: 'flex', alignItems: 'center'}}>
                        <Link target="_blank" href="https://azorian.solutions" title="Click to visit Azorian Solutions">
                            <Typography
                                variant="body1"
                                noWrap
                                sx={{
                                    mt: 0.8,
                                    mr: 2,
                                    display: {xs: 'none', md: 'flex'},
                                    fontFamily: 'roboto',
                                    fontWeight: 300,
                                    fontSize: 14,
                                    color: 'inherit',
                                    textDecoration: 'none',
                                }}
                            >
                                Created By Azorian Solutions
                            </Typography>
                        </Link>
                    </Box>
                    <Box sx={{display: 'flex', alignItems: 'center'}}>
                        <Typography
                            variant="body1"
                            noWrap
                            sx={{
                                mt: 0.8,
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'roboto',
                                fontWeight: 300,
                                fontSize: 14,
                                color: 'inherit',
                                textDecoration: 'none',
                            }}
                        >
                            Version {packageJSON.version}
                        </Typography>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
}

export default ResponsiveAppBar;
