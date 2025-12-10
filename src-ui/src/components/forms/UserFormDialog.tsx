import * as React from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {useFormik} from 'formik';
import {object, string} from 'yup';
import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Typography,
    Grid,
    Stack,
    Button,
    TextField,
    FormControl,
    FormHelperText,
    InputLabel,
    Select,
    MenuItem,

} from '@mui/material';
import {usersService} from '@app/services/system/users';

interface formRequirements {
    usernameRequired: boolean;
    usernameMinLength: number;
    usernameMaxLength: number;
    passwordRequired: boolean;
    passwordMinLength: number;
    passwordMaxLength: number;
    emailRequired: boolean;
    emailMinLength: number;
    emailMaxLength: number;
    phoneRequired: boolean;
    phoneMinLength: number;
    phoneMaxLength: number;
    statusRequired: boolean;
    tenantIdRequired: boolean;
    tenantIdLength: number;
}

const formReqs: formRequirements = {
    usernameRequired: true,
    usernameMinLength: 4,
    usernameMaxLength: 100,
    passwordRequired: true,
    passwordMinLength: 4,
    passwordMaxLength: 100,
    emailRequired: true,
    emailMinLength: 3,
    emailMaxLength: 100,
    phoneRequired: false,
    phoneMinLength: 7,
    phoneMaxLength: 15,
    statusRequired: true,
    tenantIdRequired: false,
    tenantIdLength: 32,
};

const userSchema = object({
    username: string()
        .required('Username is required.')
        .min(formReqs.usernameMinLength, `Username must be at least ${formReqs.usernameMinLength} characters.`)
        .max(formReqs.usernameMaxLength, `Username must be at most ${formReqs.usernameMaxLength} characters.`),
    password: string()
        .required('Password is required.')
        .min(formReqs.passwordMinLength, `Password must be at least ${formReqs.passwordMinLength} characters.`)
        .max(formReqs.passwordMaxLength, `Password must be at most ${formReqs.passwordMaxLength} characters.`),
    email: string()
        .required('Email is required.')
        .email('A valid email address is required.')
        .min(formReqs.emailMinLength, `Email must be at least ${formReqs.emailMinLength} characters.`)
        .max(formReqs.emailMaxLength, `Email must be at most ${formReqs.emailMaxLength} characters.`),
    phoneNumber: string()
        .min(formReqs.phoneMinLength, `Phone Number must be at least ${formReqs.phoneMinLength} digits.`)
        .max(formReqs.phoneMaxLength, `Phone Number must be at most ${formReqs.phoneMaxLength} digits.`),
    status: string()
        .required('Status is required.'),
    tenantId: string()
        .length(formReqs.tenantIdLength, 'Tenant ID is not valid.'),
});

export const FormDialog = () => {
    const [open, setOpen] = React.useState(false);
    const location = useLocation();
    const navigate = useNavigate();
    const newPath = '/create';

    const handleOpen = React.useCallback(() => {
        setOpen(true);
        const currentPath = location.pathname;

        if (!currentPath.endsWith(newPath)) {
            navigate(`${currentPath}${newPath}`);
        }
    }, [navigate, location.pathname]);

    const handleClose = React.useCallback(() => {
        setOpen(false);
        const currentPath = location.pathname;

        if (currentPath.endsWith(newPath)) {
            navigate(currentPath.slice(0, currentPath.length - newPath.length));
        }
    }, [navigate, location.pathname]);

    React.useEffect(() => {
        if (!location.pathname.endsWith(newPath)) {
            handleClose();
        } else {
            handleOpen();
        }
    }, [location, handleClose, handleOpen]);

    const form = useFormik({
        initialValues: {
            username: 'test',
            password: 'test',
            email: 'test@test.com',
            phoneNumber: '13175551234',
            status: 'active',
            tenantId: '',
        },
        validationSchema: userSchema,
        onSubmit: async (values, {setErrors, setStatus, setSubmitting}) => {
            const result = await usersService.saveRecord(values);

            if (typeof result === 'boolean' && result) {
                handleClose();
                form.resetForm();
                setStatus();
                toast.info('User saved!');
            } else if (typeof result === 'object') {
                setErrors(result);
                setStatus();
            } else {
                setStatus('User could not be saved!');
                toast.error('User could not be saved!');
            }
            setSubmitting(false);
        },
        validateOnChange: false,
        validateOnBlur: false,
    });

    return (
        <React.Fragment>
            <Button variant="contained" onClick={handleOpen}>Create User</Button>
            <Dialog
                fullWidth={true}
                maxWidth={'md'}
                open={open}
                onClose={handleClose}
            >
                <form onSubmit={form.handleSubmit} onReset={form.handleReset}>
                    <DialogTitle>Create User</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            <Typography variant="body1">Please provide the following details to create a new user and then click Save once finished.</Typography>
                            {form.status && (
                                <>
                                    <Typography variant="body1" color="error" className="formStatus">{form.status}</Typography>
                                </>
                            )}
                        </DialogContentText>
                        <Grid container marginY={2}>
                            <Grid size={{xs: 12, md: 6}}>
                                <Typography variant="h6" align="center" gutterBottom>User Information</Typography>
                                <Stack component="form" spacing={3} noValidate>
                                    <TextField
                                        label="Username"
                                        variant="outlined" // Common variant for forms
                                        fullWidth
                                        {...form.getFieldProps('username')}
                                        error={form.errors.username !== undefined}
                                        helperText={form.errors.username}
                                    />

                                    <TextField
                                        label="Password"
                                        type="password" // Masks the input for security
                                        variant="outlined"
                                        fullWidth
                                        {...form.getFieldProps('password')}
                                        error={form.errors.password !== undefined}
                                        helperText={form.errors.password}
                                    />

                                    <TextField
                                        label="Email"
                                        type="email" // Ensures correct keyboard type on mobile and basic validation
                                        variant="outlined"
                                        fullWidth
                                        {...form.getFieldProps('email')}
                                        error={form.errors.email !== undefined}
                                        helperText={form.errors.email}
                                    />

                                    <TextField
                                        label="Phone Number"
                                        type="tel" // Ensures correct keyboard type on mobile and basic validation
                                        variant="outlined"
                                        fullWidth
                                        {...form.getFieldProps('phoneNumber')}
                                        error={form.errors.phoneNumber !== undefined}
                                        helperText={form.errors.phoneNumber}
                                    />

                                    <FormControl fullWidth variant="outlined">
                                        <InputLabel id="status-label">Status</InputLabel>
                                        <Select
                                            labelId="status-label"
                                            id="status"
                                            label="Status"
                                            {...form.getFieldProps('status')}
                                            error={form.errors.status !== undefined}
                                        >
                                            <MenuItem value="">
                                                <em>None</em>
                                            </MenuItem>
                                            <MenuItem value={'pending'}>Pending</MenuItem>
                                            <MenuItem value={'invited'}>Invited</MenuItem>
                                            <MenuItem value={'active'}>Active</MenuItem>
                                            <MenuItem value={'suspended'}>Suspended</MenuItem>
                                            <MenuItem value={'disabled'}>Disabled</MenuItem>
                                        </Select>
                                        <FormHelperText>{form.errors.status}</FormHelperText>
                                    </FormControl>

                                    <FormControl fullWidth variant="outlined">
                                        <InputLabel id="tenant-label">Tenant</InputLabel>
                                        <Select
                                            labelId="tenant-label"
                                            id="tenant"
                                            label="Tenant"
                                            {...form.getFieldProps('tenantId')}
                                            error={form.errors.tenantId !== undefined}
                                        >
                                            <MenuItem value="">
                                                <em>None</em>
                                            </MenuItem>
                                            <MenuItem value={'t1'}>Tenant 1</MenuItem>
                                            <MenuItem value={'t2'}>Tenant 2</MenuItem>
                                            <MenuItem value={'t3'}>Tenant 3</MenuItem>
                                        </Select>
                                        <FormHelperText>{form.errors.tenantId}</FormHelperText>
                                    </FormControl>
                                </Stack>
                            </Grid>
                            <Grid size={{xs: 12, md: 6}}>
                                <Typography variant="h6" align="center" gutterBottom>User Roles</Typography>
                            </Grid>
                        </Grid>
                    </DialogContent>
                    <DialogActions>
                        <Button variant="contained" color="error" type="reset" onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit">Save User</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </React.Fragment>
    );
}

export default FormDialog;