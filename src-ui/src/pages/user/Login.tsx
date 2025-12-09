import {useState} from 'react';
import {Link as RouterLink} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import {toast} from 'react-toastify';
import {useFormik} from 'formik';
import {
    Box, Container, Stack, Paper, Divider, Link, Typography, Button, TextField
} from '@mui/material';
import {authService} from '@app/services/auth';
import Logo from '@app/assets/img/logo-icon.svg';
import * as React from "react";

interface formValues {
    username: string;
    password: string;
}

interface formErrors {
    username?: string;
    password?: string;
}

interface formRequirements {
    usernameMinLength: number;
    usernameMaxLength: number;
    passwordMinLength: number;
    passwordMaxLength: number;
}

const formReqs: formRequirements = {
    usernameMinLength: 4,
    usernameMaxLength: 100,
    passwordMinLength: 4,
    passwordMaxLength: 100,
};

const validate = (values: formValues) => {
    const errors: formErrors = {};
    if (!values.username) {
        errors.username = 'Your username is required';
    } else if (values.username.length > formReqs.usernameMaxLength) {
        errors.username = `Your username must be ${formReqs.usernameMaxLength} characters or less`;
    } else if (values.username.length < formReqs.usernameMinLength) {
        errors.username = `Your username must be ${formReqs.usernameMinLength} characters or more`;
    }

    if (!values.password) {
        errors.password = 'Your password is required';
    } else if (values.password.length > formReqs.passwordMaxLength) {
        errors.password = `Your password must be ${formReqs.passwordMaxLength} characters or less`;
    } else if (values.password.length < formReqs.passwordMinLength) {
        errors.password = `Your password must be ${formReqs.passwordMinLength} characters or more`;
    }

    return errors;
};

const Login = () => {
    const [t] = useTranslation();
    const [isAuthLoading, setAuthLoading] = useState(false);

    const form = useFormik({
        initialValues: {
            username: '',
            password: '',
        },
        validate,
        onSubmit: values => {
            login(values.username, values.password);
        },
    });

    const login = async (username: string, password: string) => {
        try {
            setAuthLoading(true);
            const result = await authService.login(username, password);
            if (result.id) {
                toast.success('Authentication Successful!');
            } else {
                let error = 'Authentication Failed: ';
                for (const detail of result.detail) {
                    error += detail.msg + ': ' + detail.loc[1] + ' ';
                }
                toast.error(error || 'Authentication Failed');
            }

            setAuthLoading(false);
        } catch (error: any) {
            setAuthLoading(false);
            toast.error(error.message || 'Authentication Failed');
        }
    };

    return (
        <>
            <Paper elevation={3} sx={{width: 350, padding: 2}}>
                <form onSubmit={form.handleSubmit}>
                    <Stack spacing={2}>
                        <Link href="https://dnsmin.org" target="_blank" className="h1">
                            <Typography noWrap variant="h6" className="logoText">
                                <Box sx={{display: 'flex', mt: 1.4}}>
                                    <img src={Logo} alt="DNSMin Logo" height={50}/>
                                </Box>
                                NSMin
                            </Typography>
                        </Link>

                        <Divider/>

                        <Typography variant="body1">{t('login.label.signIn')}</Typography>

                        <Stack spacing={2}>
                            <TextField id="outlined-basic" variant="outlined" label="Username"
                                       {...form.getFieldProps('username')}
                                       error={form.errors.username !== undefined}
                                       helperText={form.errors.username}
                            />

                            <TextField id="outlined-basic" variant="outlined" label="Password" type="password"
                                       {...form.getFieldProps('password')}
                                       error={form.errors.password !== undefined}
                                       helperText={form.errors.password}
                            />
                        </Stack>

                        <Container disableGutters maxWidth={false} sx={{display: 'flex', justifyContent: 'flex-end'}}>
                            <Button type="submit" loading={isAuthLoading}>
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
                </form>
            </Paper>
        </>
    );
};

export default Login;
