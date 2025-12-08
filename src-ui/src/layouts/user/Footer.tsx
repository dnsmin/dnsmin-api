import * as React from 'react';
import {useNavigate} from "react-router-dom";
import {Container, Box, AppBar, Toolbar, Typography, Link} from '@mui/material';
import Logo from "@app/assets/img/logo-icon.svg";
import packageJSON from '../../../package.json';

function ResponsiveAppBar() {
    const navigate = useNavigate();

    const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        navigate(e.currentTarget.dataset.path!);
        return true;
    };

    return (
        <AppBar color="secondary" position="fixed" elevation={0}
                sx={{
                    top: 'auto',
                    bottom: 0,
                    height: '30px',
                    paddingX: 1,
                    paddingY: 0,
                    boxShadow: 'rgba(185,185,185,1) 0 0 2px 0'
                }}>
            <Container maxWidth={false} disableGutters>
                <Toolbar disableGutters sx={{alignItems: 'flex-start', justifyContent: 'space-between'}}>
                    <Box sx={{display: 'flex', alignItems: 'center'}}>
                        <Link data-path="/" onClick={handleNavClick} sx={{mr: 1}} title="DNSMin Home">
                            <Typography noWrap variant="body1" className="logoText footer" sx={{mt: 0.5, pt: 0}}>
                                <Box sx={{display: 'flex', mt: 0.1}}>
                                    <img src={Logo} alt="DNSMin Logo" height={20}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>
                        <Typography
                            variant="body1"
                            noWrap
                            sx={{
                                mt: 0.4,
                                fontWeight: 300,
                                fontSize: 14,
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
