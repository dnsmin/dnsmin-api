import {useState} from 'react';
import {Link as RouterLink} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import {toast} from 'react-toastify';
import {
    Box, Container, Stack, Paper, Divider, Link, Typography, Button, TextField
} from '@mui/material';
import {authService} from '@app/services/auth';
import Logo from '@app/assets/img/logo-icon.svg';
import * as React from "react";

const Login = () => {
    const [t] = useTranslation();
    const [isAuthLoading, setAuthLoading] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const login = async (username: string, password: string) => {
        try {
            setAuthLoading(true);
            await authService.login(username, password);
            toast.success('Authentication Successful!');
            setAuthLoading(false);
        } catch (error: any) {
            setAuthLoading(false);
            toast.error(error.message || 'Authentication Failed');
        }
    };

    const handleSubmit = () => {
        login(username, password);
    };

    return (
        <>
            <Paper elevation={3} sx={{width: 350, padding: 2}}>
                <Stack spacing={2}>
                    <Link href="https://dnsmin.org" target="_blank" className="h1">
                        <Typography noWrap variant="h6" className="logoText">
                            <Box sx={{display: 'flex', mr: 0.1, mt: 1.4}}>
                                <img src={Logo} alt="DNSMin Logo" height={50}/>
                            </Box>
                            NSMin
                        </Typography>
                    </Link>

                    <Divider/>

                    <Typography variant="body1">{t('login.label.signIn')}</Typography>

                    <Stack spacing={2}>
                        <TextField id="outlined-basic" variant="outlined" label="Username"
                                   value={username} onChange={(e) => setUsername(e.target.value)}/>
                        <TextField id="outlined-basic" variant="outlined" label="Password"
                                   value={password} onChange={(e) => setPassword(e.target.value)}/>
                    </Stack>

                    <Container disableGutters maxWidth={false} sx={{display: 'flex', justifyContent: 'flex-end'}}>
                        <Button loading={isAuthLoading} onClick={handleSubmit}>
                            {t('login.button.signIn.label')}
                        </Button>
                    </Container>

                    <Container disableGutters maxWidth={false}>
                        <Stack spacing={1} sx={{alignItems: 'left'}}>
                            <RouterLink to="/user/forgot-password">{t('login.label.forgotPass')}</RouterLink>
                            <RouterLink to="/user/register">{t('login.label.registerNew')}</RouterLink>
                        </Stack>
                    </Container>
                </Stack>
            </Paper>
        </>
    );
};

export default Login;
