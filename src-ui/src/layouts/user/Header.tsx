import * as React from 'react';
import {useNavigate} from "react-router-dom";
import {
    Box, Container, AppBar, Toolbar, Typography, Button, IconButton, Link, Menu, MenuItem, Tooltip, Avatar
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import {authService} from "@app/services/auth";
import {useAppSelector} from '@store/store';
import Logo from '@app/assets/img/logo-icon.svg';

interface UserNav {
    label: string;
    path?: string;
    action?: string;
}

const settings: UserNav[] = [
    {label: 'Profile', path: '/user/profile'},
    {label: 'Security', path: '/user/security'},
    {label: 'Logout', action: 'logout'},
];

function ResponsiveAppBar() {
    const navItems = useAppSelector((state) => state.ui.navItems);
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

    const handleCloseUserMenu = (e: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(null);
        if (e.currentTarget.dataset.path!) {
            navigate(e.currentTarget.dataset.path!);
        }
        if (e.currentTarget.dataset.action!) {
            if (e.currentTarget.dataset.action === 'logout') {
                authService.logout();
            }
        }
    };

    const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        setAnchorElNav(null);
        navigate(e.currentTarget.dataset.path!);
        return true;
    };

    return (
        <AppBar color="secondary" position="sticky" elevation={1} sx={{paddingX: 1, boxShadow: '0 0 2px rgba(185,185,185,1)'}}>
            <Toolbar disableGutters>
                <Container sx={{paddingX: 1, display: 'flex', alignItems: 'center'}}>
                    <Box sx={{flexGrow: 0, display: {xs: 'none', md: 'flex'}, mr: 5}}>
                        <Link data-path="/" onClick={handleNavClick} title="DNSMin">
                            <Typography noWrap variant="h6" className="logoText">
                                <Box sx={{display: 'flex', mr: 0.1, mt: 1.4}}>
                                    <img src={Logo} alt="DNSMin Logo" height={50}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>
                    </Box>
                    <Box sx={{flexGrow: 0, display: {xs: 'none', md: 'flex'}}}>
                        {navItems.map((ni, index) => (
                            <Button
                                key={index}
                                href="#"
                                data-path={ni.path}
                                onClick={handleNavClick}
                                className="headerNav"
                                sx={{my: 2, mx: 2, display: 'block'}}
                            >
                                {ni.label}
                            </Button>
                        ))}
                    </Box>
                    <Box sx={{flexGrow: 1, display: {xs: 'flex', md: 'none'}}}>
                        <IconButton
                            size="large"
                            aria-label="Open Menu"
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
                        <Link data-path="/" onClick={handleNavClick} title="DNSMin">
                            <Typography noWrap variant="body1" className="logoText">
                                <Box sx={{display: 'flex', mt: 1.1}}>
                                    <img src={Logo} alt="DNSMin Logo" height={50}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>
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
                            {settings.map((setting, index) => (
                                <MenuItem key={index} data-path={setting.path} data-action={setting.action}
                                          onClick={handleCloseUserMenu}>
                                    <Typography sx={{textAlign: 'center'}}>{setting.label}</Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                </Container>
            </Toolbar>
        </AppBar>
    );
}

export default ResponsiveAppBar;
