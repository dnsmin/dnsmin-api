import * as React from 'react';
import {useNavigate} from "react-router-dom";
import {
    Box, Container, AppBar, Toolbar, Typography, Button, IconButton, Link, Menu, MenuItem, Tooltip, Avatar
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Logo from '@app/assets/img/logo1-icon.svg';

const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

interface navItem {
    label: string;
    path: string;
    children?: [navItem];
}

const navItems: navItem[] = [
    {label: 'Home', path: '/'},
    {label: 'Home 2', path: '/home2'},
    {label: 'Settings', path: '/settings'},
    {label: 'System', path: '/system'},
    {label: 'Servers', path: '/servers'},
    {label: 'Zones', path: '/zones'},
    {label: 'Audits', path: '/audits'},
];

function ResponsiveAppBar() {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
    const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);
    const navigate = useNavigate();

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        setAnchorElNav(null);
        navigate(e.currentTarget.dataset.path!);
        return true;
    };

    return (
        <AppBar position="sticky">
            <Container maxWidth={false} disableGutters sx={{paddingX: 1}}>
                <Toolbar disableGutters>
                    <Link data-path="/" onClick={handleNavClick} title="DNSMin Home">
                        <Typography
                            variant="h6"
                            noWrap
                            sx={{
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: 'inherit',
                                textDecoration: 'none',
                            }}
                        >
                            <Box sx={{display: {xs: 'none', md: 'flex'}, mr: 0.5}}>
                                <img src={Logo} alt="DNSMin Logo" height={30}/>
                            </Box>
                            NSMin
                        </Typography>
                    </Link>

                    <Box sx={{flexGrow: 1, display: {xs: 'flex', md: 'none'}}}>
                        <IconButton
                            size="large"
                            aria-label="Open User Menu"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleOpenNavMenu}
                            color="inherit"
                        >
                            <MenuIcon/>
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{display: {xs: 'block', md: 'none'}}}
                        >
                            {navItems.map((ni, index) => (
                                <MenuItem key={index} href="#" data-path={ni.path} onClick={handleNavClick}>
                                    <Typography sx={{textAlign: 'center'}}>{ni.label}</Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                    <Box sx={{flexGrow: 1, display: {xs: 'flex', md: 'none'}}}>
                        <Link data-path="/" onClick={handleNavClick} title="DNSMin Home">
                            <Typography
                                variant="h5"
                                noWrap
                                sx={{
                                    mr: 2,
                                    display: {xs: 'flex', md: 'none'},
                                    flexGrow: 1,
                                    fontFamily: 'monospace',
                                    fontWeight: 700,
                                    letterSpacing: '.3rem',
                                    color: 'inherit',
                                    textDecoration: 'none',
                                }}
                            >
                                <Box sx={{display: {xs: 'flex', md: 'none'}, mr: 0.5}}>
                                    <img src={Logo} alt="DNSMin Logo" height={30}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>
                    </Box>
                    <Box sx={{flexGrow: 1, display: {xs: 'none', md: 'flex'}}}>
                        {navItems.map((ni, index) => (
                            <Button
                                key={index}
                                href="#"
                                data-path={ni.path}
                                onClick={handleNavClick}
                                sx={{my: 2, display: 'block'}}
                            >
                                {ni.label}
                            </Button>
                        ))}
                    </Box>
                    <Box sx={{flexGrow: 0}}>
                        <Tooltip title="Open User Menu">
                            <IconButton onClick={handleOpenUserMenu} sx={{p: 0}}>
                                <Avatar alt="DNSMin User" src="/img/default-profile.png"/>
                            </IconButton>
                        </Tooltip>
                        <Menu
                            sx={{mt: '45px'}}
                            id="menu-appbar"
                            anchorEl={anchorElUser}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            open={Boolean(anchorElUser)}
                            onClose={handleCloseUserMenu}
                        >
                            {settings.map((setting) => (
                                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                                    <Typography sx={{textAlign: 'center'}}>{setting}</Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
}

export default ResponsiveAppBar;
